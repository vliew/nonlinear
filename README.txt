This folder contains the pseudo-Boolean multiplier benchmarks and their generators for the paper "Verifying Properties of Bit-vector Multiplication Using Cutting Planes Reasoning".

We include instances for each problem for 9-32 or more bits. To generate instances of arbitrary bit-width, place the corresponding generator into the same folder as "circuits_pb.py". 
Then run from the command line, for example:

>> python genPB_array_diag 64

to produce a 64-bit instance to check equivalence of array and diagonal multipliers.

The solver Sat4j-CP is currently available at https://www.sat4j.org/

The solvers Sat4j-divto1 and RoundingSat2 used are not yet publicly available.