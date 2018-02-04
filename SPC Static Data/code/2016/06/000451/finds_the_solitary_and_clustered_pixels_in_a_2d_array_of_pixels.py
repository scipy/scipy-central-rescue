# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 15:43:07 2016
Upgraded on Wed march 03 14:00:30 2013 - Version 3
Following some user requests:
- slight polishing of the outputs by adding an output vector of the sequence
of the clusters
- C version for fast processing (see bottom of python script )
@author: lautrido
"""
import numpy as np
import time

###############################################################################
def findclu(dimx, dimy, Pos):
    """
    FINDCLU finds the solitary and clustered pixels in a 2D array of pixels.
    Recognition of these structures is commonly used in processing of ionizing
    particles in pixelated detectors or of CCDs in astrophysics.

    ---PURPOSE---
    The function provides the ordered lists of solitary and clustered pixels.
    A Cluster is defined by the assembly of adjoining pixels (neighbors).
    An isolated pixel is a pixel having no neighbors. Neighbors of the pixel
    P[i,j] are defined as the 8 pixels of the sub-array P[i-1:i+1, j-1:j+1].
    The function can rapidly process large 2D arrays having a large number of
    solitaries and large sizes of clusters.

    ---INPUT---
    dimx = number of rows of the array of pixels (int)
    dimy = number of columns of the array of pixels (int)
    Pos = numpy 2D array (of int16) of the indices of positions of the selected
          pixels, ranked following [[list of row indexes], [list of column
          indexes]]
    (see demo script below)

    ---OUTPUT---
    Sol = numpy 2D array (of int16) of the ordered indices of positions of the
          solitary pixels, ranked following [[list of row indexes], [list of
          column indexes]]
    Clu = numpy 2D array (of int16) of the ordered indices of positions of the
          clustered pixels, ranked following [[list of row indexes], [list of
          column indexes]], and ordered by the vector Seq.
	Seq = Numpy 1D array (of int32) giving the sequences of the lengths of the
		 clusters stored in Clu.
    (see demo script below)

    ---USAGE---
    Sol, Clu, Seq = findclu(dimx, dimy, Pos)

    ---AUTHOR---
    P. Lautridou (2017) (Pascal.Lautridou@subatech.in2p3.fr)
    Tested with python 3.5.1, numpy 1.11.1 - Matlab version also available
    C version available at bottom of the script
    """

    import numpy as np

    # print("Number of input pixels:",np.shape(Pos)[1])
    dimx2, dimy2 = dimx+2, dimy+2
    H = np.full((dimx2, dimy2), False, dtype=bool)
    Pos = Pos + 1
    H[Pos[0, :], Pos[1, :]] = True #index=y+x*dimy2

# Search of the neighbors (cf. Scipy central: 100 numpy exercices)
    V = (H[:-2, :-2] | H[:-2, 1:-1] | H[:-2, 2:] | H[1:-1, :-2] |
         H[1:-1, 2:] | H[2:, :-2] | H[2:, 1:-1] | H[2:, 2:])

# Search of the solitaries
    V = np.logical_and(np.logical_not(V), H[1:-1, 1:-1])
    # 2D-array Sol = Coodinates [[raw],[col]] of the solitary pixels
    Sol = np.int16((np.nonzero(V)))
    print("Number of solitary pixels:", np.shape(Sol)[1])

# Search of the clusters
    H[1:-1, 1:-1] = np.logical_xor(H[1:-1, 1:-1], V)
    Hf = np.int32(np.flatnonzero(H))
    nhit = np.shape(Hf)[0]
    print("Number of clustered pixels:", nhit)
    if nhit<2:
        Clu = np.array([], np.int16)
        Seq = np.array([], np.int32)
        return Sol, Clu, Seq

    V = np.zeros((dimx2, dimy2), np.int32)
    V[Hf // dimy2, Hf % dimy2] = Hf
    for k in range(nhit):
        i = (Hf[k] // dimy2) - 1
        j = (Hf[k] % dimy2) - 1
        V[i:i+3, j:j+3] = H[i:i+3, j:j+3] * V[i+1,j+1]

    for k in range(nhit):
        i = (Hf[k] // dimy2) - 1
        j = (Hf[k] % dimy2) - 1
        for m in range(i, i+3):
            for n in range(j, j+3):
                if (V[m,n] > 0) and (V[m,n] != V[i+1, j+1]):
#                    B=np.int32(np.where(V==V[m,n]))
#                    V[B[0],B[1]] = V[i+1, j+1]
                    V[V==V[m,n]] = V[i+1, j+1]

    Vf = V[V>0]
    U, Seq = np.unique(Vf, return_counts=True)
    Clu = np.array([], np.int32)
    for i in U:
        Clu = np.append(Clu, Hf[Vf==i])
    print("Number of clusters:", np.size(Seq))
    print("Largest cluster size:", np.amax(Seq), "pixels")
    # 2D array Clu = Coodinates [[row],[col]] of the clustered pixels
    Clu = np.int16([Clu // dimy2, Clu % dimy2])-1

    return Sol, Clu, Seq

            ###################################################

# Demo with a 2D array of dimension (dimx, dimy),
# and the following coordinates (row,col) of the selected pixels:
# (0,0); (0,2); (1,4); (1,1); (2,0); (4,0); (4,2); (4,3); (4,4)

dimx, dimy = 5, 6

# coordinates array in format [[row],[col]]
Pos = np.array([[0,0,1,1,2,4,4,4,4], [0,2,4,1,0,0,2,3,4]], dtype = np.int16)
print(Pos)
t1 = time.clock()
Sigl, Neig, Nbr = findclu(dimx, dimy, Pos)
t2 = time.clock()
print("Runing time:", t2-t1)
print("Solitaries", Sigl)
print("Cluster sequence ", Nbr)
print("Clusters", Neig)

"""

###############################################################################
                           C VERSION
###############################################################################

#include <stdio.h>
#include <stdlib.h>

void findclu(int *, int *, int *, int, int, int);

int main()
{
//	test for findclu
    int const dimx=5, dimy=5;
    int nhit=9;
    int Seq[nhit];
    int X[9] = {0,0,1,1,2,4,4,4,4}; // hit locations in the pixel matrix
    int Y[9] = {0,2,4,1,0,0,2,3,4};

    findclu(X, Y, Seq, nhit, dimx, dimy);

    for (int i=0; i<nhit; i++)
    {
        printf("Nb %3d\n",Seq[i]); // see sequence of cluster
    }
    for (int i=0; i<nhit; i++)
    {
        printf("X %3d\n",X[i]); // see location sequence
    }
    for (int i=0; i<nhit; i++)
    {
        printf("Y %3d\n",Y[i]);
    }
}

/////////////////////////////////////////////////////////////////////
void findclu(int *X, int *Y, int *Nb, int nhit, int dimx, int dimy)
{

/**
Inputs:
- X, Y: vectors of int and length nhit, containing the indexes
  of the pixels in the pixel matrix processed
- Nb: vector of int and length nhit, for output
- nhit: integer, the number of hits
- dimx, dimy: integers, dimensions of the pixel matrix(dimx,dimy)
  processed

Outputs:
- X, Y: reordered according to Nb;
- Nb: contains the sequence and the lengths of the clusters:
      Nb[0] gives the number of solitary pixels
      Nb[i> 0] gives the number of pixels of the cluster i
      until Nb[j] = -1 is reached

For example, an output vector Nb=[2, 4, 3, -1, -1,...] indicates that:
- there are 2 solitary pixels (Nb[0]=2) and the Nb[0] first elements
  of X (and Y) contain the row (column) indices of these solitaries
- there are 2 clusters: Nb[1]=4 (4 pixels cluster), and Nb[2]=3
  (3 pixels cluster)
- Nb[3]=-1 (Nb[3] to Nb[nhit-1]=-1) indicates there is no more clusters.
The re-ordering of X (row indices) in output is the following (idem in Y):
X=[sol_1, sol_2, clust_1_pix_1, clust_1_pix_2, clust_1_pix_3,
   clust_1_pix_4, clust_2_pix_1, clust_2_pix_2, clust_2_pix_3].

So, the rule of locations in X is (idem in Y):
- for the solitaries: from item X[0] to X[Nb[0]-1];
- for the first cluster: from item X[Nb[0]] to
  X[Nb[0]+Nb[1]-1];
- for the second cluster (if existing): from item X[Nb[0]+Nb[1]] to
  X[Nb[0]+Nb[1]+Nb[2]-1].
  etc.

If Nb[0]=0 (and necessarily for an non empty matrix: Nb[i>0]>0):
=> there is no solitary => no corresponding item in X and Y;
- information of first cluster remain from item X[Nb[0]] to
  X[Nb[0]+Nb[1]-1];
- information on second cluster (if existing) remain from item
  X[Nb[0]+Nb[1]] to X[Nb[0]+Nb[1]+Nb[2]-1].
  etc.
**/

//  Dimension of the extended working mat
    int dimx2 = dimx + 2, dimy2 = dimy + 2;
    int i, j, k, m, n, ii, jj, kk;

//  Init of the vector of the sequences of the clusters
    for (i=0; i<nhit; i++) { Nb[i] = -1; }

//  Init of the boolean working mat
    char **H = (char **) malloc(dimx2*sizeof(char *));
    if (H == NULL)
    {
        fprintf(stderr,"findclu: Memory allocation aborted\n");
        exit(EXIT_FAILURE);
    }
    H[0] = (char *) calloc(dimy2*dimx2, sizeof(char));
    if (H[0] == NULL)
    {
        fprintf(stderr,"findclu: Memory allocation aborted\n");
        exit(EXIT_FAILURE);
    }
    for (i = 1 ; i<dimx2 ; i++) { H[i] = H[i-1] + dimy2; }
// Load H with the pixel positions
    for (i=0; i<nhit; i++) { H[X[i]+1][Y[i]+1] = 1; }

// Init of second working mat
    char **V = (char **) malloc(dimx2*sizeof(char *));
    if (V == NULL)
    {
        fprintf(stderr,"findclu: Memory allocation aborted\n");
        exit(EXIT_FAILURE);
    }
    V[0] = (char *) calloc(dimy2*dimx2, sizeof(char));
    if (V[0] == NULL)
    {
        fprintf(stderr,"findclu: Memory allocation aborted\n");
        exit(EXIT_FAILURE);
    }
    for (i=1 ; i<dimx2 ; i++) V[i] = V[i-1] + dimy2;

// Neighbors calculation
    for (i=1; i<dimx2-1; i++)
    {
        for (j=1; j<dimy2-1; j++)
        {
            V[i][j] = H[i-1][j-1] || H[i-1][j] || H[i-1][j+1] || \
                      H[i][j-1] || H[i][j+1] || \
                      H[i+1][j-1] || H[i+1][j] || H[i+1][j+1];
        }
    }

// find and release solitary pixels
    int nsol = 0;
    for (i=1; i<dimx2-1; i++)
    {
        for (j=1; j<dimy2-1; j++)
        {
            V[i][j] = H[i][j] && (!V[i][j]);
            if (V[i][j] != 0)
            {
                X[nsol] = i - 1; /* back to initial indices */
                Y[nsol] = j - 1;
                nsol+= 1;
            }
        }
    }
    printf ("Number of solitary pixels: %7d\n",nsol);
//  Save number of solitaries inside Nb
    Nb[0] = nsol;

// If no clustered pixel, return
    if (nsol == nhit) {return;}

// Otherwise start search of the clusters
    int iclu = nhit - nsol;
    printf ("Number of clustered pixels: %7d\n",iclu);

// Init of the vector of H flattened and non-zero, Lig, Col for the indice locations
    int *Hf = malloc(iclu * sizeof(int *));
    if (Hf == NULL)
    {
        fprintf(stderr,"findclu: Memory allocation aborted\n");
        exit(EXIT_FAILURE);
    }
    int *Lig = malloc( iclu * sizeof(int *));
    if (Lig == NULL)
    {
        fprintf(stderr,"findclu: Memory allocation aborted\n");
        exit(EXIT_FAILURE);
    }
    int *Col = malloc( iclu * sizeof(int *));
    if (Col == NULL)
    {
        fprintf(stderr,"findclu: Memory allocation aborted\n");
        exit(EXIT_FAILURE);
    }

// find the clustered pixels
    k = 0;
    for (i=1; i<dimx2-1; i++)
    {
        for (j=1; j<dimy2-1; j++)
        {
            H[i][j] = H[i][j] ^ V[i][j];
            if (H[i][j] != 0)
            {
                Hf[k] = j + i * dimy2;
                Lig[k] = i;
                Col[k] = j;
                k+= 1;
            }
        }
    }
    free(*V); /* delete V and H*/
    free(V);
    free(*H);
    free(H);

    // Init of a working mat
    int **W = (int **) malloc(dimx2*sizeof(int *));
    if (W == NULL)
    {
        fprintf(stderr,"findclu: Memory allocation aborted\n");
        exit(EXIT_FAILURE);
    }
    W[0] = (int *) calloc(dimy2*dimx2, sizeof(int));
    if (W[0] == NULL)
    {
        fprintf(stderr,"findclu: Memory allocation aborted\n");
        exit(EXIT_FAILURE);
    }
    for (i = 1 ; i < dimx2 ; i++) W[i] = W[i-1] + dimy2;

// Load W with Hf
    for (k=0; k<iclu; k++) W[ Lig[k] ][ Col[k] ] = Hf[k];

// Find the clusters, applying the two-stage filter
    for (k=0; k<iclu; k++)
    {
        i = Lig[k];
        j = Col[k];
        for (m=i-1; m<i+2; m++)
        {                                /* apply the filter */
            for (n=j-1; n<j+2; n++) W[m][n] = (W[m][n] != 0) * W[i][j];
        }

    }

    int W0;
    for (k=0; k<iclu; k++)
    {
        i = Lig[k];
        j = Col[k];
        for (m=i-1; m<i+2; m++)
        {
            for (n=j-1; n<j+2; n++)
            {
                if ((W[m][n] != 0) && (W[m][n] != W[i][j]))
                {
                    W0 = W[m][n];
                    for (kk=0; kk<iclu; kk++)
                    {
                        ii = Lig[kk];
                        jj = Col[kk];   /* re-apply the filter */
                        if (W[ii][jj] == W0) { W[ii][jj] = W[i][j];}
                    }
                }
            }
        }
    }

// Load Hf with W values flattened and non-zero
    for (k=0; k<iclu; k++) Hf[k] = W[ Lig[k] ][ Col[k] ];

    free(*W); /* bye-bye W */
    free(W);

// Sort and release clustered pixels and clusters
    int nclu = 1, ihit = 0;
    k = nsol;
    for (i=0; i<iclu; i++)
    {
        if (Hf[i] != 0)
        {
            X[k] = Lig[i] - 1;
            Y[k] = Col[i] - 1;
            k+= 1;
            ihit+= 1;
            for (j=i+1; j<iclu; j++)
            {
                if (Hf[j] == Hf[i])
                {
                    Hf[j] = 0;
                    X[k] = Lig[j] - 1;
                    Y[k] = Col[j] - 1;
                    k+=1;
                    ihit+= 1;
                }
            }
            Nb[nclu] = ihit; /* output of the sequence of the cluster */
            nclu+= 1;
            ihit = 0;
        }
    }
    free(Hf); /* bye-bye Hf, Lig, Col */
    free(Lig);
    free(Col);

    printf ("Number of clusters: %7d\n", nclu-1);
    int max = 0;
    for (k=1; k<nclu+1; k++)
    {
        if (Nb[k] > max) { max = Nb[k]; }
    }
    printf ("Largest cluster size (in pixel): %7d\n", max);

    return;
}

"""