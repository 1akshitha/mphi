#! /usr/bin/env python3
def prime_mpi ( ):
  import numpy as np
  import platform
  import sys
  from mpi4py import MPI

  comm = MPI.COMM_WORLD

  id = comm.Get_rank ( )

  p = comm.Get_size ( )

  n_lo = 1
  n_hi = 1000000
  n_factor = 2

  if id == 0:
    wtime = MPI.Wtime ( )
    print ( '' )
    print ( 'PRIME_MPI' )
    print ( '  Python version: %s' % ( platform.python_version ( ) ) )
    print ( '  Count the primes between %d and %d' % ( n_lo, n_hi ))
    print ( '' )
    print ( '  Use MPI to divide the computation among' )
    print ( '  multiple processes.' )
#
#  Search the range [2,N] for  primes.
#  After each search, double N and do it again.
#
  n = n_lo

  while n <= n_hi:
#
#  The PRIMES array starts out as an empty list of integers.
#
    primes = np.array ( 0, dtype = np.int32 )
    wtime = MPI.Wtime ( )
#
#  T is the sum of resiprocals of primes
#
    t = 0
#
#  Process 0 checks   2+0,   2+0  +P, 2+0  +2P  ...
#  Process 1 checks   2+1,   2+1  +P, 2+1  +2P, ...
#  Process P-1 checks 2+P-1, 2+P-1+P, 2+P-1+2P, ... 
#
    for i in range ( 2 + id, n + 1, p ):
      isprime = 1
      for j in range ( 2, i ):
        if ( i % j ) == 0:
          isprime = 0
          break
      t = t + isprime*(1/i) #if it is a prime, resiprocal is added.

    comm.Reduce ( [ t, MPI.DOUBLE ], [ primes, MPI.INT ], op = MPI.SUM, root = 0 )

    wtime = MPI.Wtime ( ) - wtime

    if id == 0:
      print ( '  %d  %d  %g', ( n, primes, wtime ) )

    n = n * n_factor
#
#  Terminate.
#
  if id == 0:
    print ( '' )
    print ( 'PRIME_MPI:' )
    print ( '  Normal end of execution.' )

  return

def timestamp ( ):

#*****************************************************************************80
  import time

  t = time.time ( )
  print ( time.ctime ( t ) )

  return None

def timestamp_test ( ):

#*****************************************************************************80
  import platform

  print ( '' )
  print ( 'TIMESTAMP_TEST:' )
  print ( '  Python version: %s' % ( platform.python_version ( ) ) )
  print ( '  TIMESTAMP prints a timestamp of the current date and time.' )
  print ( '' )

  timestamp ( )
#
#  Terminate.
#
  print ( '' )
  print ( 'TIMESTAMP_TEST:' )
  print ( '  Normal end of execution.' )
  return

if ( __name__ == '__main__' ):
  timestamp ( )
  prime_mpi ( )
  timestamp ( )