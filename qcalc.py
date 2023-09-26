# Quantum Calculator
# The Quantum Calculator is a Maple program that can carry out computations in the small quantum cohomology ring of any Grassmannian of classical type. More precisely, it covers ordinary Grassmannians (type A) and Grassmannians of isotropic subspaces in a symplectic vector space (type C) or in an orthogonal vector space (type B or D). This software was written as part of a joint project with Andrew Kresch and Harry Tamvakis, aimed at studying the small quantum cohomology rings of submaximal isotropic and orthogonal Grassmannians. The Quantum Calculator is open source software (under the GNU General Public License).

# To use the Quantum Calculator, download the file qcalc, place it in the current directory, and issue the Maple commands "read qcalc;" and "with(qcalc);". This makes several functions available. A detailed description can be found in the User Manual. The following example gives an impression of the capabilities:

# % maple
#     |\^/|     Maple 10 (IBM INTEL LINUX)
# ._|\|   |/|_. Copyright (c) Maplesoft, a division of Waterloo Maple Inc. 2005
#  \  MAPLE  /  All rights reserved. Maple is a trademark of
#  <____ ____>  Waterloo Maple Inc.
#       |       Type ? for help.
# > read qcalc:
# > with(qcalc):
# > Gr(3,7):
# > qtoS(S[2,1]^3);
#      4 S[4, 4, 1] + 8 S[4, 3, 2] + 2 S[3, 3, 3] + 5 q S[2] + 4 q S[1, 1]
# I will be grateful for any comments or bug reports regarding this package. Thanks to Weihong Xu for one such report. Enjoy!

import numpy as np
from typing import *

# qcalc := module()
# option package;

# export
#   set_type, get_type, Gr, IG, OG, type_string,
#   schub_classes, generators, point_class, all_kstrict,
#   pieri, act, giambelli, mult, toS,
#   qpieri, qact, qgiambelli, qmult, qtoS,
#   dualize, type_swap, miami_swap, schub_type,
#   part2pair, pair2part, part2index, index2part, apply_lc;

# local _k, _n, _type, _pieri, _qpieri, fail_no_type, _dcoef,
#   spec2num, num2spec, giambelli_rec_inner, giambelli_rec, act_lc,
#   pieri_set, count_comps, _pieri_fillA, _pieri_itrA,
#   _pieri_fill, _pieri_itr, _part_star,
#   _part_tilde, part2pair_inner, pair2part_inner,
#   type_swap_inner, miami_swap_inner, dualize_index_inner,
#   part2indexA_inner, part2indexC_inner, part2indexB_inner, part2indexD_inner,
#   index2partA_inner, index2partC_inner, index2partB_inner, index2partD_inner,
#   part_len, part_clip, part_conj, part_itr, part_itr_between,
#   _first_kstrict, _itr_kstrict,
#   pieriA_inner, pieriC_inner, pieriB_inner, pieriD_inner,
#   qpieriA_inner, qpieriC_inner, qpieriB_inner, qpieriD_inner;


# ##################################################################
# # Common interface for all types
# ##################################################################

# fail_no_type := proc()
#   ERROR("Must set type with IG or OG or set_type functions.");
# end:

# _type   := false:
# _k      := false:
# _n      := false:
# _pieri  := fail_no_type:
# _qpieri := fail_no_type:

# set_type := proc(tp, k, n)
#   if k<0 or n<k then ERROR("Need 0 <= k <= n."); fi;
#   if tp = "A" then
#     _pieri  := pieriA_inner;
#     _qpieri := qpieriA_inner;
#   elif tp = "C" then
#     _pieri  := pieriC_inner;
#     _qpieri := qpieriC_inner;
#   elif tp = "B" then
#     _pieri  := pieriB_inner;
#     _qpieri := qpieriB_inner;
#   elif tp = "D" then
#     _pieri  := pieriD_inner;
#     _qpieri := qpieriD_inner;
#   else
#     fail_no_type();
#   fi;
#   _k      := k;
#   _n      := n;
#   _type   := tp;
#   type_string();
# end:

# type_string := proc()
#   local td;
#   td := get_type();
#   sprintf("Type %s ;  (k,n) = (%d,%d) ;  %s(%d,%d) ;  deg(q) = %d", op(td));
#   # sprintf("Type %s ;  %s(%d,%d) ;  deg(q) = %d", td[1], op(4..-1,td));
# end:

# get_type := proc()
#   if _type = "A" then
#     ["A", _k, _n, "Gr", _n-_k, _n, _n];
#   elif _type = "C" then
#     ["C", _k, _n, "IG", _n-_k, 2*_n, _n+1+_k];
#   elif _type = "B" then
#     ["B", _k, _n, "OG", _n-_k, 2*_n+1, `if`(_k=0,2*_n,_n+_k)];
#   elif _type = "D" then
#     ["D", _k, _n, "OG", _n+1-_k, 2*_n+2, `if`(_k=0,2*_n,_n+_k)];
#   else
#     fail_no_type();
#   fi;
# end:

# Gr := proc(m, N)
#   set_type("A", N-m, N);
# end:

# IG := proc(m, N)
#   if N mod 2 = 1 then ERROR("Second argument must be even."); fi;
#   set_type("C", N/2-m, N/2);
# end:

# OG := proc(m, N)
#   if N mod 2 = 1 then
#     set_type("B", (N-1)/2-m, (N-1)/2);
#   else
#     set_type("D", N/2-m, N/2-1);
#   fi;
# end:

# schub_classes := proc()
#   local res, mu;
#   if not type(_type,string) then fail_no_type() fi;
#   if _type="A" then
#     res := {};
#     mu := [_k$(_n-_k)];
#     while type(mu,list) do
#       res := res union {S[op(part_clip(mu))]};
#       mu := part_itr(mu);
#     od;
#     res;
#   elif _type="D" then
#     `union`(op(map(mu->`if`(member(_k,mu), {S[op(mu)],S[op(mu),0]},
#     {S[op(mu)]}), all_kstrict(_k, _n+1-_k, _n+_k))));
#   else
#     map(lam -> S[op(lam)], all_kstrict(_k,_n-_k,_n+_k));
#   end:
# end:

# generators := proc()
#   local i;
#   if not type(_type,string) then fail_no_type() fi;
#   if _type<>"D" and _k=_n then RETURN([]); fi;
#   [seq(S[i],i=1.._k),`if`(_type="D" and _k>0,S[_k,0],NULL),
#    `if`(_type<>"A",seq(S[i],i=_k+1.._n+_k),NULL)];
# end:

# point_class := proc()
#   local i;
#   if not type(_type,string) then fail_no_type() fi;
#   if _type="A" then RETURN(S[`if`(_k>0,_k$(_n-_k),NULL)]); fi;
#   S[seq(_n+_k-i, i=0.._n-_k-`if`(_type="D" and _k>0,0,1))];
# end:

# part2pair := proc(lc)
#   if _type="A" then ERROR("Only types B,C,D."); fi;
#   if type(lc,list) then
#     part2pair_inner(lc);
#   else
#     apply_lc(lam->part2pair_inner(lam,_k), lc);
#   fi;
# end:

# pair2part := proc(lc)
#   if _type="A" then ERROR("Only types B,C,D."); fi;
#   if type(lc,list) and nops(lc)=2 then
#     pair2part_inner(lc);
#   else
#     apply_lc(pair->pair2part_inner(pair), lc);
#   fi;
# end:

# part2index := proc(lc)
#   if type(lc,list) then RETURN(part2index(S[op(lc)])); fi;
#   if _type="A" then
#     apply_lc(lam->part2indexA_inner(lam,_k,_n), lc);
#   elif _type="C" then
#     apply_lc(lam->part2indexC_inner(lam,_k,_n), lc);
#   elif _type="B" then
#     apply_lc(lam->part2indexB_inner(lam,_k,_n), lc);
#   elif _type="D" then
#     apply_lc(lam->part2indexD_inner(lam,_k,_n), lc);
#   else
#     fail_no_type();
#   fi;
# end:

# index2part := proc(lc)
#   if type(lc,list) then RETURN(index2part(S[op(lc)])); fi;
#   if _type="A" then
#     apply_lc(idx->index2partA_inner(idx,_k,_n), lc);
#   elif _type="C" then
#     apply_lc(idx->index2partC_inner(idx,_k,_n), lc);
#   elif _type="B" then
#     apply_lc(idx->index2partB_inner(idx,_k,_n), lc);
#   elif _type="D" then
#     apply_lc(idx->index2partD_inner(idx,_k,_n), lc);
#   else
#     fail_no_type();
#   fi;
# end:

# dualize := proc(lc)
#   local N;
#   N := `if`(_type="A",_n,
#        `if`(_type="C", 2*_n, `if`(_type="B", 2*_n+1, 2*_n+2)));
#   index2part(apply_lc(idx->dualize_index_inner(idx,N,_type),
#     part2index(lc)));
# end:

# type_swap := proc(lc)
#   if type(lc,list) then RETURN(type_swap(S[op(lc)])); fi;
#   if _type="D" then
#     apply_lc(lam->type_swap_inner(lam,_k), lc);
#   else
#     lc;
#   fi;
# end:

# miami_swap := proc(lc)
#   if type(lc,list) then RETURN(miami_swap(S[op(lc)])); fi;
#   if _type="D" then
#     apply_lc(lam->miami_swap_inner(lam,_k), lc);
#   else
#     lc;
#   fi;
# end:

# schub_type := proc(lam)
#   if not type(_type,string) then fail_no_type() fi;
#   if _type<>"D" or not (type(lam,list) or type(lam,indexed)) then
#     ERROR("No type defined.");
#   fi;
#   if not member(_k,{op(lam)}) then
#     0;
#   elif nops(lam)=0 or op(-1,lam)>0 then
#     1;
#   else
#     2;
#   fi;
# end:

# pieri := proc(i, lc)
#   if type(lc,list) then
#     _pieri(i, lc, _k, _n)
#   else
#     apply_lc(p->_pieri(i,p,_k,_n), lc);
#   fi;
# end:

# act := proc(expr, lc)
#   act_lc(expr, lc, (i,p)->_pieri(i,p,_k,_n));
# end:

# giambelli := proc(lc)
#   giambelli_rec(lc, (i,p)->_pieri(i,p,_k,_n), _k);
# end:

# mult := proc(lc1, lc2)
#   act(giambelli(lc1), lc2);
# end:

# toS := proc(lc)
#   act(giambelli(lc), S[]);
# end:

# qpieri := proc(i, lc)
#   if type(lc,list) then
#     _qpieri(i, lc, _k, _n)
#   else
#     apply_lc(p->_qpieri(i,p,_k,_n), lc);
#   fi;
# end:

# qact := proc(expr, lc)
#   act_lc(expr, lc, (i,p)->_qpieri(i,p,_k,_n));
# end:

# qgiambelli := proc(lc)
#   giambelli_rec(lc, (i,p)->_qpieri(i,p,_k,_n), _k);
# end:

# qmult := proc(lc1, lc2)
#   qact(qgiambelli(lc1), lc2);
# end:

# qtoS := proc(lc)
#   qact(qgiambelli(lc), S[]);
# end:


# ##################################################################
# # Type A: Quantum cohomology of Gr(n-k,n).
# ##################################################################

# pieriA_inner := proc(i, lam, k,n)
#   option remember;
#   local inner, outer, mu, res;
#   inner := [op(lam), 0$(n-k-nops(lam))];
#   outer := [k,op(1..-2,inner)];
#   mu    := _pieri_fillA(inner, inner, outer, 1, i);
#   res := 0;
#   while type(mu,list) do
#     res := res + S[op(part_clip(mu))];
#     mu := _pieri_itrA(mu, inner, outer);
#   od;
#   res;
# end:

# qpieriA_inner := proc(i, lam, k,n)
#   local res, lab, j;
#   res := pieriA_inner(i, lam, k,n);
#   if nops(lam)=n-k and lam[n-k]>0 then
#     if k=1 then RETURN(q*S[]); fi;
#     lab := [seq(`if`(lam[j]>1, lam[j]-1, NULL), j=1..nops(lam))];
#     res := res + expand(q * apply_lc(x->_part_star(x,k-1),
#            pieriA_inner(i-1,lab,k-1,n)));
#   fi;
#   res;
# end:


# ##################################################################
# # Type C: Quantum cohomology of symplectic IG(n-k,2n).
# ##################################################################

# pieriC_inner := proc(i, lam, k,n)
#   option remember;
#   convert(map(x->2^count_comps(lam,x,true,k,0)*S[op(x)],
#           pieri_set(i,lam,k,n,0)),`+`);
# end:

# qpieriC_inner := proc(i, lam, k,n)
#   pieriC_inner(i, lam, k,n) +
#   expand(q/2 * apply_lc(x->_part_star(x,n+k+1), pieriC_inner(i, lam, k, n+1)));
# end:


# ##################################################################
# # Type B: Quantum cohomology of odd orthogonal OG(n-k,2n+1).
# ##################################################################

# pieriB_inner := proc(p, lam, k,n)
#   option remember;
#   local b;
#   b := `if`(p <= k, 0, 1);
#   convert(map(mu -> 2^(count_comps(lam,mu,false,k,0)-b) * S[op(mu)],
#     pieri_set(p,lam,k,n,0)), `+`);
# end:

# qpieriB_inner := proc(p, lam, k,n)
#   local res;
#   res := pieriB_inner(p, lam, k,n);

#   if k=0 then
#     if nops(lam)>0 and lam[1]=n+k then
#       res := res + q * apply_lc(x->_part_star(x,n+k),
#         pieriB_inner(p,[op(2..-1,lam)],k,n));
#     fi;
#   else
#     if nops(lam)=n-k and lam[n-k]>0 then
#       res := res + q * apply_lc(x->_part_tilde(x,n-k+1,n+k),
#         pieriB_inner(p, lam, k,n+1));
#     fi;
#     if nops(lam)>0 and lam[1]=n+k then
#       res := res + q^2 * apply_lc(x->_part_star(x,n+k),
#         pieriB_inner(p,[op(2..-1,lam)],k,n));
#     fi;
#   fi;
#   expand(res);
# end:


# ##################################################################
# # Type D: Quantum cohomology of even orthogonal OG(n+1-k,2n+2).
# ##################################################################

# pieriD_inner := proc(p, lam, k,n)
#   option remember;
#   local tlam;
#   tlam := `if`(not member(k,lam), 0, `if`(lam[-1]=0, 2, 1));
#   convert(map(mu -> _dcoef(p,lam,mu,tlam,k,n),
#     pieri_set(abs(p),lam,k,n,1)), `+`);
# end:

# _dcoef := proc(p, lam, mu, tlam, k,n)
#   local cc, h, pmu, i, tmu, lami;
#   cc := count_comps(lam, mu, false, k,1) - `if`(abs(p)<k, 0, 1);
#   if cc >= 0 then
#     if not member(k,mu) or tlam=1 then
#       2^cc*S[op(mu)]
#     elif tlam=2 then
#       2^cc*S[op(mu),0]
#     else
#       2^cc*S[op(mu)] + 2^cc*S[op(mu),0]
#     fi;
#   else
#     # Tie breaking
#     h := k + tlam + `if`(p<0,1,0);
#     pmu := 0;
#     for i from nops(mu) to 1 by -1 while pmu < k do
#       lami := `if`(i <= nops(lam), lam[i], 0);
#       if lami<min(mu[i],k) then
#         h := h - (min(mu[i],k) - max(pmu,lami));
#       fi;
#       pmu := mu[i];
#     od;
#     h := h mod 2;
#     if tlam=0 and member(k,mu) then
#       S[op(mu), 0$h];
#     elif h=0 then
#       0;
#     else
#       S[op(mu), `if`(tlam=2 and member(k,mu), 0, NULL)];
#     fi;
#   fi;
# end:

# qpieriD_inner := proc(p, lam, k,n)
#   local res, lb, cprd, intn, x, res1;
#   res := pieriD_inner(p, lam, k,n);

#   if k=0 then
#     if nops(lam)>0 and lam[1]=n+k then
#       res := res + q * apply_lc(x->_part_star(x,n+k),
#         pieriD_inner(p, [op(2..-1,lam)], k,n));
#     fi;
#   elif k=1 then
#     if nops(lam)>=n and lam[n]>0 then
#       lb := part_clip([seq(max(x-1,0),x=lam)]);
#       cprd := `if`(abs(p)>1, pieriD_inner(abs(p)-1,lb,0,n), S[op(lb)]);
#       intn := {seq(i,i=1..n)};
#       cprd := apply_lc(mu ->
#               S[op(ListTools[Reverse]([op(intn minus {op(mu)})]))], cprd);
#       res1 := 0;
#       if lam[-1]>0 and p>0 then
#         res1 := q1*apply_lc(mu -> S[seq(x+1,x=mu),1$(n-nops(mu))], cprd);
#       fi;
#       if (lam[-1]=0 or not member(k,lam)) and (p=-1 or p>1) then
#         res1:=res1 + q2*apply_lc(mu-> S[seq(x+1,x=mu),1$(n-nops(mu)),0],cprd);
#       fi;
#       res := res + dualize(res1);
#     fi;
#     if nops(lam)>0 and lam[1]=n+k then
#       res := res + q1*q2 * apply_lc(x->_part_star(x,n+k),
#         pieriD_inner(p, [op(2..-1,lam)], k,n));
#     fi;
#   else
#     if nops(lam)>=n+1-k and lam[n+1-k]>0 then
#       res := res + q * type_swap(apply_lc(x->_part_tilde(x,n-k+2,n+k),
#         pieriD_inner(p, lam, k,n+1)), k);
#     fi;
#     if nops(lam)>0 and lam[1]=n+k then
#       res := res + q^2 * apply_lc(x->_part_star(x,n+k),
#         pieriD_inner(p, [op(2..-1,lam)], k,n));
#     fi;
#   fi;
#   expand(res);
# end:


# ##################################################################
# # General cohomology calculations, depending on Pieri rule.
# ##################################################################

# spec2num := proc(sc)
#   if (not type(sc,indexed)) or op(0,sc)<>`S` or nops(sc)=0 then
#     ERROR("special schubert class expected");
#   fi;
#   if nops(sc)>1 and (_type<>"D" or op(2,sc)<>0) then
#     ERROR("single part expected");
#   fi;
#   `if`(nops(sc)>1, -op(1,sc), op(1,sc));
# end:

# num2spec := proc(p)
#   `if`(p>0, S[p], S[-p,0]);
# end:

# apply_lc := proc(f, lc)
#   if type(lc, `+`) or type(lc, `*`) or type(lc, `^`) then
#     RETURN(expand(map2(apply_lc, f, lc)));
#   elif type(lc, indexed) and op(0,lc) = `S` then
#     RETURN(f([op(lc)]));
#   else
#     RETURN(lc);
#   fi;
# end:

# act_lc := proc(expc, lc, pieri)
#   local vars, v, i, expc0, expc1;
#   vars := indets(expc) minus {q};
#   if nops(vars) = 0 then
#     RETURN(expc * lc);
#   fi;
#   v := vars[1];
#   i := spec2num(v);
#   expc0 := subs(v=0, expc);
#   expc1 := expand((expc - expc0) / v);
#   apply_lc(p->pieri(i,p), act_lc(expc1,lc,pieri)) + act_lc(expc0,lc,pieri);
# end:

# giambelli_rec_inner := proc(lam, pieri, k)
#   option remember;
#   local p, lam0, stuff;
#   if nops(lam)=0 then RETURN(1); fi;
#   p := lam[1];
#   if p=k and lam[-1]=0 then p := -k; fi;
#   lam0 := [op(2..`if`(lam[-1]=0 and lam[2]<k,-2,-1), lam)];
#   stuff := pieri(p, lam0) - S[op(lam)];
#   expand(num2spec(p) * giambelli_rec_inner(lam0, pieri, k) -
#          giambelli_rec(stuff, pieri, k));
# end:

# giambelli_rec := proc(lc, pieri, k)
#   apply_lc(x->giambelli_rec_inner(x,pieri,k), lc);
# end:


# ##################################################################
# # Pieri rule internals
# ##################################################################

# _pieri_fillA := proc(lam, inner, outer, r, p)
#   local res, pp, rr, x;
#   if nops(lam) = 0 then RETURN(lam); fi;
#   res := array(lam);
#   pp := p;
#   rr := r;
#   if rr = 1 then
#     x := min(outer[1], inner[1]+pp);
#     res[1] := x;
#     pp := pp - x + inner[1];
#     rr := 2;
#   fi;
#   while rr <= nops(lam) do
#     x := min(outer[rr], inner[rr]+pp, res[rr-1]);
#     res[rr] := x;
#     pp := pp - x + inner[rr];
#     rr := rr + 1;
#   od;
#   if pp > 0 then RETURN(false); fi;
#   [seq(res[rr], rr=1..nops(lam))];
# end:

# _pieri_itrA := proc(lam, inner, outer)
#   local p, r, lam1;
#   if nops(lam) = 0 then RETURN(false); fi;
#   p := lam[-1] - inner[-1];
#   for r from nops(lam)-1 to 1 by -1 do
#     if lam[r] > inner[r] then
#       lam1 := subsop(r=lam[r]-1, lam);
#       lam1 := _pieri_fillA(lam1, inner, outer, r+1, p+1);
#       if lam1 <> false then RETURN(lam1); fi;
#       p := p + lam[r] - inner[r];
#     fi;
#   od;
#   false;
# end:

# count_comps := proc(lam1, lam2, skipfirst, k,d)
#   local top1,bot1, top2,bot2, lb2, comps, i,j,b, res, incomp, minj,maxj;

#   top1 := part_conj([seq(min(lam1[i],k), i=1..nops(lam1))]);
#   top1 := [op(top1), 0$(k-nops(top1))];
#   bot1 := [op(part_clip([seq(max(0,lam1[i]-k), i=1..nops(lam1))])), 0];
#   top2 := part_conj([seq(min(lam2[i],k), i=1..nops(lam2))]);
#   top2 := [op(top2), 0$(k-nops(top2))];
#   bot2 := part_clip([seq(max(0,lam2[i]-k), i=1..nops(lam2))]);

#   lb2 := nops(bot2);
#   if lb2 = 0 then RETURN(0); fi;
#   comps := array([0$bot2[1]]);
#   for i from 1 to lb2 do
#     for j from bot1[i]+1 to bot2[i] do
#       comps[j] := 1;
#     od;
#   od;

#   b := 1;
#   for i from 1 to k do
#     if top2[i] <= top1[i] then
#       while b < lb2 and bot1[b]+b-1 > top1[i]+k-i-d do b := b+1; od;
#       minj := top2[i]+k-i-b+2-d;
#       maxj := min(top1[i]+k-i-b+2-d, bot2[1]);
#       for j from minj to maxj do
#         comps[j] := -1;
#       od;
#     fi;
#   od;
#   res := 0;
#   incomp := skipfirst;
#   for j from 1 to bot2[1] do
#     if comps[j]=1 and not incomp then
#       res := res + 1;
#     fi;
#     incomp := evalb(comps[j]=1);
#   od;
#   RETURN(res);
# end:

# pieri_set := proc(p, lam, k,n,d)
#   local top, bot, top1, top_1, top1c, bot1, bot_1, inner, outer,
#         b, i, j, ti, res, p1, topk, top1k, inbot, outbot, b1, lbot, rows,cols;
#   rows := n+d-k;
#   cols := n+k;

#   # Split up in PR partition pairs (to reuse old code).
#   top := part_conj([seq(min(lam[i],k), i=1..nops(lam))]);
#   top := [op(top), 0$(k-nops(top))];
#   topk := `if`(k=0, cols, top[k]);
#   bot := [op(part_clip([seq(max(0,lam[i]-k), i=1..nops(lam))])), 0];
#   lbot := nops(bot)-1;

#   # Find bounds for new top partition
#   outer := [seq(min(rows,top[j]+1), j=1..k)];
#   inner := `if`(k=0, [],
#     [seq(max(lbot,top[j+1]), j=1..nops(top)-1), lbot]);
#   b := 1;
#   for i from 1 to k do
#     while b <= lbot and bot[b]+b-1 > top[i]+k-i-d do b := b+1; od;
#     if top[i]+k-i+2-b-d <= 0 then
#       inner := subsop(i=max(top[i],inner[i]), inner);
#     else
#       inner := subsop(i=max(bot[b]+b-1+i-k+d,inner[i]), inner);
#     fi;
#   od;

#   # Iterate through all possible top partitions
#   res := {};
#   top_1 := outer;
#   while type(top_1, list) do
#     top1 := top_1;
#     top_1 := part_itr_between(top1, inner, outer);
#     p1 := p + `+`(op(top)) - `+`(op(top1));
#     if p1 < 0 then next; fi;

#     # Obvious bounds for bottom partition
#     top1k := `if`(k=0, rows, top1[k]);
#     inbot := [op(1..lbot,bot), `if`(lbot<top1k,0,NULL)];
#     if lbot=0 then
#       outbot := `if`(top1k>0, [cols-k], []);
#     else
#       outbot := [cols-k,op(1..lbot-1,bot),`if`(lbot<top1k,bot[lbot],NULL)];
#     fi;

#     # Find exact bounds for bottom partition, using shift-under conditions.
#     b := 1;
#     for i from 1 to k do
#       if top1[i] <= top[i] then
#         while b <= lbot and bot[b]+b-1 > top[i]+k-i-d do b := b+1; od;
#         if top1[i] < top[i] then
#           if b > nops(inbot) then
#             inbot := false;
#             break;
#           fi;
#           inbot := subsop(b = max(inbot[b],top[i]+k-i-b+2-d), inbot);
#         fi;
#         b1 := b;
#         while b1 < nops(outbot) and bot[b1]+b1-1 <= top[i]+k-i-d do
#           outbot := subsop(b1+1 = min(outbot[b1+1],top1[i]+k-i-b1-d), outbot);
#           b1 := b1+1;
#         od;
#       fi;
#     od;

#     # Check if top partition didn't work after all.
#     if inbot = false then next; fi;
#     j := `+`(op(bot));
#     if `+`(op(outbot)) - j < p1 then next; fi;
#     p1 := p1 - `+`(op(inbot)) + j;
#     if p1 < 0 then next; fi;

#     # Iterate through all valid bottom partitions.
#     bot1 := _pieri_fill(inbot, inbot, outbot, 1, p1);
#     top1c := part_conj(top1);
#     while type(bot1, list) do
#       if k=0 then
#         res := res union {part_clip(bot1)};
#       else
#         j := min(nops(top1c), nops(bot1));
#         res := res union
#                {[seq(top1c[i]+bot1[i],i=1..j), op(j+1..nops(top1c),top1c)]};
#       fi;
#       bot1 := _pieri_itr(bot1, inbot, outbot);
#     od;
#   od;
#   res;
# end:

# _pieri_fill := proc(lam, inner, outer, r, p)
#   local res, pp, rr, x;
#   if nops(lam) = 0 then RETURN(lam); fi;
#   res := array(lam);
#   pp := p;
#   rr := r;
#   if rr = 1 then
#     x := min(outer[1], inner[1]+pp);
#     res[1] := x;
#     pp := pp - x + inner[1];
#     rr := 2;
#   fi;
#   while rr <= nops(lam) do
#     x := min(outer[rr], inner[rr]+pp, res[rr-1]-1);
#     res[rr] := x;
#     pp := pp - x + inner[rr];
#     rr := rr + 1;
#   od;
#   if pp > 0 then RETURN(false); fi;
#   [seq(res[rr], rr=1..nops(lam))];
# end:

# _pieri_itr := proc(lam, inner, outer)
#   local p, r, lam1;
#   if nops(lam) = 0 then RETURN(false); fi;
#   p := lam[-1] - inner[-1];
#   for r from nops(lam)-1 to 1 by -1 do
#     if lam[r] > inner[r] then
#       lam1 := subsop(r=lam[r]-1, lam);
#       lam1 := _pieri_fill(lam1, inner, outer, r+1, p+1);
#       if lam1 <> false then RETURN(lam1); fi;
#       p := p + lam[r] - inner[r];
#     fi;
#   od;
#   false;
# end:

# _part_star := proc(lam, cols)
#   if nops(lam)=0 or lam[1]<>cols then RETURN(0); fi;
#   S[op(2..-1,lam)];
# end:

# _part_tilde := proc(lam, rows,cols)
#   local r;
#   if part_len(lam)<>rows or lam[1]>cols then RETURN(0); fi;
#   r := rows + lam[1] - cols;
#   if r <= 0 then RETURN(0); fi;
#   if r<rows and lam[r+1]>1 then RETURN(0); fi;
#   S[op(2..r,lam), `if`(lam[-1]=0,0,NULL)];
# end:





# ##################################################################
# # Miscellaneous conversions
# ##################################################################
def _first_kstrict(k: int, rows: int, cols: int) -> Optional[List[int]]:
    return [max(k, cols - i) for i in range(rows)]


def _itr_kstrict(lambda_: List[int], k: int) -> Optional[List[int]]:
    n = len(lambda_)
    i = n
    
    while i > 0 and lambda_[i-1] == 0:
        i -= 1

    if i == 0:
        return None
    
    li = lambda_[i-1] - 1
    
    if li <= k:
        return lambda_[:i-1] + [li] * (n - i + 1)
    elif li + i - n > k:
        return lambda_[:i-1] + [li - j for j in range(n - i + 1)]
    else:
        return lambda_[:i-1] + [li - j for j in range(li - k + 1)] + [k] * (n - i - li + k)


def part_clip(lambda_: List[int]) -> Optional[List[int]]:
    i = len(lambda_) - 1  # zero-based indexing in Python
    while i >= 0 and lambda_[i] == 0:
        i -= 1

    return lambda_[:i+1] if i >= 0 else None


def all_kstrict(k: int, rows: int, cols: int) -> Set[Tuple[int, ...]]:
    res = set()
    lam = _first_kstrict(k, rows, cols)
    
    while isinstance(lam, list): # Check if lam is a list
        clipped = part_clip(lam)
        if clipped:  # Check if clipped is not None
            res.add(tuple(clipped))
        lam = _itr_kstrict(lam, k)

    return res


def part_conj(lambda_: List[int]) -> List[int]:
    n = len(lambda_)
    if n == 0:
        return []
    else:
        m = lambda_[0]
        res = [0] * m
        j = 1
        for i in range(m, 0, -1):
            while j < n and lambda_[j] >= i:
                j += 1
            res[i - 1] = j
        return res
    

def part_itr(mu: List[int]) -> Optional[List[int]]:
    i = len(mu) - 1
    while i >= 0 and mu[i] == 0:
        i -= 1
    if i < 0:
        return None
    a = mu[i] - 1
    return mu[:i] + [a] * (len(mu) - i)


# tau < mu < lambda
def part_itr_between(mu: List[int], tau: List[int], lambda_: List[int]) -> Optional[List[int]]:
    i = len(mu) - 1
    while i >= 0 and mu[i] == tau[i]:
        i -= 1

    if i < 0:
        return None

    return mu[:i] + [min(mu[j]-1, lambda_[j]) for j in range(i, len(mu))]


def part_len(lambda_: List[int]) -> int:
    n = len(lambda_) - 1
    while n >= 0 and lambda_[n] == 0:
        n -= 1
    return n + 1



# ##################################################################
# # Miscellaneous conversions
# ##################################################################

def part2pair_inner(lam: List[int], k: int) -> Tuple[List[int], List[int]]:
    top = part_conj([min(i, k) for i in lam])
    bot = part_clip([max(i - k, 0) for i in lam])

    # Adjust lengths
    top.extend([0] * (k - len(top)))
    
    if len(lam) > 0 and lam[-1] == 0:
        bot.append(0)

    return top, bot

# pair2part_inner := proc(pair)
#   local lam, np2, i;
#   if nops(op(1,pair))=0 then RETURN(S[op(op(2,pair))]); fi;
#   lam := part_conj(op(1,pair));
#   np2 := nops(op(2,pair));
#   S[seq(lam[i]+op(2,pair)[i], i=1..np2), op(np2+1..-1,lam),
#     `if`(np2>0 and op(2,pair)[-1]=0, 0, NULL)];
# end:

# miami_swap_inner := proc(lam, k)
#   local i;
#   if not member(k, {op(lam)}) then RETURN(S[op(lam)]); fi;
#   if `+`(seq(`if`(op(i,lam)>k,1,0), i=1..nops(lam))) mod 2 = 0 then
#     RETURN(S[op(lam)]);
#   fi;
#   if op(-1,lam)=0 then
#     S[op(1..-2,lam)];
#   else
#     S[op(lam),0];
#   fi;
# end:

# type_swap_inner := proc(lam, k)
#   if nops(lam)=0 then
#     S[];
#   elif not member(k,lam) then
#     # FIXME: Very ugly code to delete extra zero from typeless partitions.
#     # It is here to make the "illegal" k=1 case of qpieriD work.
#     if op(-1,lam)=0 then S[op(1..-2,lam)] else S[op(lam)]; fi;
#   elif op(-1,lam)=0 then
#     S[op(1..-2,lam)];
#   else
#     S[op(lam),0];
#   fi;
# end:

# part2indexA_inner := proc(lam, k, n)
#   local la, j;
#   la := [op(lam), 0$(n-k)];
#   S[seq(k+j-la[j], j=1..n-k)];
# end:

# part2indexC_inner := proc(lam, k, n)
#   local la, i, j;
#   la := [op(lam), 0$(n-k)];
#   S[seq(n+k+1-la[j]+`+`(seq(`if`(la[i]+la[j] <= 2*k+j-i,1,0),
#     i=1..j-1)), j=1..n-k)];
# end:

# part2indexB_inner := proc(lam, k, n)
#   local la, i, j;
#   la := [op(lam), 0$(n-k)];
#   S[seq(`if`(la[j]>k, n+k+1-la[j], n+k+2-la[j] +
#     `+`(seq(`if`(la[i]+la[j] <= 2*k+j-i,1,0), i=1..j-1))), j=1..n-k)];
# end:

# part2indexD_inner := proc(lam, k, n)
#   local la, i, j, nt;
#   la := [op(lam),0$(n+1-k)];
#   nt := n + `if`(nops(lam)>0 and lam[-1]=0, 2, 1);
#   S[seq(n+k-la[j] + `+`(seq(`if`(la[i]+la[j] <= 2*k-1+j-i, 1,0), i=1..j-1)) +
#     `if`(la[j]>k or (la[j]=k and (j=1 or k<la[j-1]) and (nt+j mod 2)=0), 1, 2),
#     j=1..n+1-k)];
# end:

# index2partA_inner := proc(idx, k, n)
#   local j, la;
#   la := [seq(k+j-idx[j], j=1..n-k)];
#   S[op(part_clip(la))];
# end:

# index2partC_inner := proc(idx, k, n)
#   local i, j, la;
#   la := [seq(n+k+1-op(j,idx)+`+`(seq(`if`(op(i,idx)+op(j,idx) > 2*n+1,1,0),
#     i=1..j-1)), j=1..n-k)];
#   S[op(part_clip(la))];
# end:

# index2partB_inner := proc(idx, k, n)
#   local i, j, la;
#   la := [seq(`if`(op(j,idx)<=n, n+k+1-op(j,idx), n+k+2-op(j,idx) +
#     `+`(seq(`if`(op(i,idx)+op(j,idx) > 2*n+2,1,0),i=1..j-1))), j=1..n-k)];
#   S[op(part_clip(la))];
# end:

# index2partD_inner := proc(idx, k, n)
#   local i, j, la, ii;
#   la := part_clip([seq(`if`(op(j,idx) <= n+1, n+k+1-op(j,idx),
#     n+k+2-op(j,idx) + `+`(seq(`if`(op(i,idx)+op(j,idx) > 2*n+3,1,0),
#     i=1..j-1))), j=1..n+1-k)]);
#   if not member(k,la) then RETURN(S[op(la)]); fi;
#   S[op(la), `if`(nops({ii$ii=1..n+1} minus {op(idx)}) mod 2 = 1, 0, NULL)];
# end:

# dualize_index_inner := proc(idx, N, tp)
#   local i, res;
#   res := S[seq(N+1-op(-i,idx),i=1..nops(idx))];
#   if tp="D" and N/2 mod 2 = 1 then
#     res := subs({N/2=N/2+1,N/2+1=N/2}, res);
#   fi;
#   res;
# end: