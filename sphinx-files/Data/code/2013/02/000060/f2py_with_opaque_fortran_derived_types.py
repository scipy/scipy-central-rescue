# License: Creative Commons Zero (almost public domain) http://scpyce.org/cc0

# 8<----- _test.f90
module foo
  use iso_c_binding
  type, bind(c) :: something_t
     integer(c_signed_char) :: a
     real(c_double) :: b, c
     integer(c_int) :: d, e, f
  end type something_t
  integer, parameter :: something_t_size = 4 + 2*8 + 3*4  ! careful with alignment

  !! You might also do just this, but it is less safe:
  !
  !type something_t
  !   integer*1 :: a
  !   double precision :: b, c
  !   integer :: d, e, f
  !end type something_t
  !integer, parameter :: something_t_size = 64  ! = 1 + 2*8 + 3*4 + safety margin

end module foo

subroutine something_init(p, a, b, c, d, e, f)
  use foo
  implicit none
  !f2py integer*1, dimension(something_t_size) :: p
  type(something_t), intent(out) :: p
  integer*1 :: a
  double precision :: b, c
  integer :: d, e, f
  p%a = a
  p%b = b
  p%c = c
  p%d = d
  p%e = e
  p%f = f
end subroutine something_init
  
subroutine do_something(p)
  use foo
  implicit none
  !f2py integer*1, dimension(something_t_size) :: p
  type(something_t), intent(in) :: p
  write(*,*) p%a, p%b, p%c, p%d, p%e, p%f
end subroutine do_something
# 8<----- _test.f90


# 8<----- test.py
import numpy as np
import _test

# This is more or less safe
p = _test.something_init(1, 2, 3, 4, 5, 6)
_test.do_something(p)

# The following is compiler-dependent, UNLESS you use 
# the bind(c) form for the type definition.
dt = np.dtype([('a', 'i1'), ('b', 'd'), ('c', 'd'), ('d', 'i'), ('e', 'i'), ('f', 'i')], align=True)
p = p.view(dt).view(np.recarray)
print p.a, p.b, p.c, p.d, p.e

# 8<----- _test.f90

$ f2py -c -m _test _test.f90
$ python test.py
   1.0000000000000000        2.0000000000000000                3           4           5
[1] [ 2.] [ 3.] [4] [5]
