#!/bin/bash
R=10
for i in {1..9}; do java -jar negsel2.jar -self syscalls/snd-unm/$R/snd-unm.train -n $R -r $i -c -l < syscalls/snd-unm/$R/snd-unm.1.test > syscalls/snd-unm/$R/scores/snd-unm.1.$i.txt; done
for i in {1..9}; do java -jar negsel2.jar -self syscalls/snd-unm/$R/snd-unm.train -n $R -r $i -c -l < syscalls/snd-unm/$R/snd-unm.2.test > syscalls/snd-unm/$R/scores/snd-unm.2.$i.txt; done
for i in {1..9}; do java -jar negsel2.jar -self syscalls/snd-unm/$R/snd-unm.train -n $R -r $i -c -l < syscalls/snd-unm/$R/snd-unm.3.test > syscalls/snd-unm/$R/scores/snd-unm.3.$i.txt; done
