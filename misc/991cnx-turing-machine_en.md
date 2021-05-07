<!--title:Turing Machine for CASIO fx-991CNX-->
<!--description: -->
<!--creationDate: 20201215-->

# Input
The machine has 3 states and a tape length of 32 bits.  
The tape is encoded in binary in the variable $B$, where position 0 is the lowest bit.  
The transition function is stored in $A$, in the following format:  
- Define `OUTPUT` as a 4-bit block consisting of `[next_state(2 bits)][movement direction(1 bit)][number to write(1 bit)]` where:
  - $\text{next_state} \in [0,3]$, jumping to state 3 will halt the machine.
  - $\text{movement} \in [0,1]$, where 0 decreses R/W head position by one and 1 increases it by one.
  - $\text{number_to_write} \in [0,1]$, the number to write to the tape (before movement)
- $A$ consists of 6 blocks of `OUTPUT`, resembling the outcome of the following scenario (from low bit to high):
  - At state 0, now reads 0
  - At state 0, now reads 1
  - At state 1, now reads 0
  - At state 1, now reads 1
  - At state 2, now reads 0
  - At state 2, now reads 1

The machine will first write, then move, then possibly halt.

# Program
$\text{transition function} \rightarrow A$  
$\text{tape} \rightarrow B$  
$\text{start state} \rightarrow C$  
$\text{start position} \rightarrow D$  

$\sqrt{2-C}\sqrt{31-D}\sqrt{D} :$  
$(1-(-1)^{B\div R 2^D}) \rightarrow x :$  
$B-2^Dx \rightarrow B :$  
$4x+8C \rightarrow x :$  
$B+(1-(-1)^{A\div R 2^x})\div2\times2^D \rightarrow B :$  
$D-(-1)^{A\div R 2^{x+1}} \rightarrow D :$  
$A\div R 2^{x+2}-A\div R2^{x+4}\times4 \rightarrow C$

# Example Programs

## The first machine
$A=195$, $C=0$, $D=0$  
Reads 0 and write 1 till the first 1, then write 0 and halt.

## Two's compliment
$A=26482$, $C=0$, $D=0$  
Calculates the two's compliment of the number in $B$.

## Lowbit
$A=26226$, $C=0$, $D=0$  
Just $B=lowbit(B)$.

## Bit flip
$A=35$, $C=0$, $D=0$  
Flip all bits.

# Compatibility
By replacing all "$\div R$"s with the "$Rnd()$" function and setting rounding to Fixed 0, this code should also work on fx-991ES or even fx-82ES.