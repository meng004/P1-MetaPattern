# N5 industrial MR corpora (expert-approved) — BAMBOO-C (SPARK, LOCUST) + SACOS

> Provenance: supplied by the author as **expert-approved** metamorphic relations for
> two production nuclear codes, for the N5 out-of-domain transferability task.
> Source files: `SPARK_LOCUST_*.docx` (BAMBOO-C core: SPARK steady-state/depletion +
> LOCUST lattice/assembly), `SACOS_*.doc` (sub-channel thermal-hydraulics).
> Transcribed verbatim from the documents (docx XML / WPS OLE2 UTF-16LE extraction).
> Expert approval = J1 (validity) given for all entries (this is Arm B of the N5
> protocol). The documents themselves split each corpus into "expert-identified" and
> "newly discovered / implicit" subsets (recorded below).

All relations are of the metamorphic form `r: <input ordering> , R: <output ordering>`
(a change in one input, with the implied covariation of an output): i.e. **monotone
covariation** relations.

---

## SPARK (BAMBOO-C core; steady-state / depletion)

Glossary: Bu burnup, dBu burnup increment, CBC critical boron conc., AO axial offset,
R0 control-rod position, Fq hot-channel factor, DBC boron differential worth,
ITC isothermal temp coef, MTC moderator temp coef, DTC Doppler temp coef,
S source strength, D detector response, Fuel_heat, ρ coolant density, EIGEN eigenvalue,
TCin/TCout coolant in/out temp, nor_Power normalised power, Pr power.

```
MR1: r:R01<R02, R:CBC1<CBC2
MR2: r:R01>R02, R:CBC1>CBC2
MR3: r:R01<R02, R:EIGEN1<EIGEN2
MR4: r:R01>R02, R:EIGEN1>EIGEN2
MR5: r:Bu1<Bu2, R:CBC1>CBC2
MR6: r:Bu1>Bu2, R:CBC1<CBC2
MR7: r:TCin1<TCin2, R:TCout1<TCout2
MR8: r:TCin1>TCin2, R:TCout1>TCout2
MR9: r:TCin1<TCin2, R:CBC1>CBC2
MR10: r:TCin1>TCin2, R:CBC1<CBC2
MR11: r:TCin1<TCin2, R:EIGEN1>EIGEN2
MR12: r:TCin1>TCin2, R:EIGEN1<EIGEN2
MR13: r:nor_Power1<nor_Power2, R:CBC1>CBC2
MR14: r:nor_Power1>nor_Power2, R:CBC1<CBC2
MR15: r:Pr1<Pr2, R:CBC1>CBC2
MR16: r:Pr1>Pr2, R:CBC1<CBC2
MR17: r:Pr1<Pr2, R:TCout1<TCout2
MR18: r:Pr1>Pr2, R:TCout1>TCout2
MR19: r:Fuel_heat1<Fuel_heat2, R:CBC1>CBC2
MR20: r:Fuel_heat1>Fuel_heat2, R:CBC1<CBC2
MR21: r:Fuel_heat1<Fuel_heat2, R:TCout1<TCout2
MR22: r:Fuel_heat1>Fuel_heat2, R:TCout1>TCout2
MR23: r:Fuel_heat1<Fuel_heat2, R:CBC1<CBC2
MR24: r:Fuel_heat1>Fuel_heat2, R:CBC1>CBC2
MR25: r:Fuel_heat1<Fuel_heat2, R:TCout1>TCout2
MR26: r:Fuel_heat1>Fuel_heat2, R:TCout1<TCout2
MR27: r:Fuel_heat1<Fuel_heat2, R:CBC1>CBC2
MR28: r:Fuel_heat1>Fuel_heat2, R:CBC1<CBC2
MR29: r:Fuel_heat1<Fuel_heat2, R:TCout1<TCout2
MR30: r:Fuel_heat1>Fuel_heat2, R:TCout1>TCout2
MR31: r:S1<S2, R:D1<D2
MR32: r:S1>S2, R:D1>D2
MR33: r:Tfuel1<Tfuel2, R:DTC1>DTC2
MR34: r:Tfuel1>Tfuel2, R:DTC1<DTC2
MR35: r:ρ1<ρ2, R:MTC1>MTC2
MR36: r:ρ1>ρ2, R:MTC1<MTC2
```
Split: MR1-MR30 expert-identified; MR31-MR36 newly discovered.
Note: MR23/MR27 and MR25 appear with overlapping antecedents in the source (Fuel_heat
vs CBC/TCout); transcribed verbatim, flagged for source clarification (does not change
block classification).

---

## LOCUST (BAMBOO-C; lattice / assembly)

Glossary: Tfuel fuel temp, Burn burnup, Enrich enrichment, Boron boron conc.,
TBoron moderator temp, Poison burnable-poison density, Control control rod,
Location, Npoison poison-cell count; outputs: Keff, Power, L cell size, t depletion time.

```
MR1: r:Tfuel1<Tfuel2, R:Keff1>Keff2
MR2: r:Tfuel1>Tfuel2, R:Keff1<Keff2
MR3: r:Burn1<Burn2, R:Keff1>Keff2
MR4: r:Burn1>Burn2, R:Keff1<Keff2
MR5: r:Enrich1<Enrich2, R:Keff1<Keff2
MR6: r:Enrich1>Enrich2, R:Keff1>Keff2
MR7: r:Boron1<Boron2, R:Keff1>Keff2
MR8: r:Boron1>Boron2, R:Keff1<Keff2
MR9: r:Boron1<threshold AND TBoron1<TBoron2, R:Keff1>Keff2
MR10: r:Boron1<threshold AND TBoron1>TBoron2, R:Keff1<Keff2
MR11: r:Boron1>threshold AND TBoron1<TBoron2, R:Keff1<Keff2
MR12: r:Boron1>threshold AND TBoron1>TBoron2, R:Keff1>Keff2
MR13: r:Poison1<Poison2, R:Keff1>Keff2
MR14: r:Poison1>Poison2, R:Keff1<Keff2
MR15: r:Control1<Control2, R:Keff1>Keff2
MR16: r:Control1>Control2, R:Keff1<Keff2
MR17: r:Control1<Control2, R:Power1>Power2
MR18: r:Control1>Control2, R:Power1<Power2
MR19: r:Npoison1<Npoison2, R:Keff1>Keff2
MR20: r:Npoison1>Npoison2, R:Keff1<Keff2
MR21: r:Burn1<Burn2 AND dT_same, R:dKeff2>dKeff1
MR22: r:Burn1>Burn2 AND dT_same, R:dKeff2<dKeff1
MR23: r:L1<L2, R:Keff1>Keff2
MR24: r:L1>L2, R:Keff1<Keff2
MR25: r:t1<t2, R:Keff1>Keff2
MR26: r:t1>t2, R:Keff1<Keff2
MR27: r:Npoison1<Npoison2, R:Keff1>Keff2
MR28: r:Npoison1>Npoison2, R:Keff1<Keff2
```
Split: MR1-MR22 expert-identified; MR23-MR28 newly discovered.
Sub-types: MR9-MR12 conditional (regime split on a Boron threshold, sign flip);
MR21-MR22 increment / second-order (ordering of the Keff *increment* vs burnup).

---

## SACOS (sub-channel thermal-hydraulics)

Glossary: To channel-exit temp, Rb equilibrium quality, Rv void fraction,
Lf grid-spacer coef, Vf channel flow velocity, Fps flow rate, Tm turbulent-mixing coef,
T temp, Rf quality, P total power, Tin inlet temp, Po outlet pressure,
Pa channel overall pressure, Kform local-resistance coef (appears as "Kfrom" in source),
Re Reynolds number.

```
MR1: r:Fps1>Fps2, R:To1<To2
MR2: r:Fps1<Fps2, R:To1>To2
MR3: r:Fps1>Fps2, R:Rb1<Rb2
MR4: r:Fps1<Fps2, R:Rb1>Rb2
MR5: r:Fps1>Fps2, R:Rv1<Rv2
MR6: r:Fps1<Fps2, R:Rv1>Rv2
MR7: r:Tin1>Tin2, R:To1>To2
MR8: r:Tin1<Tin2, R:To1<To2
MR9: r:Tin1>Tin2, R:Rb1>Rb2
MR10: r:Tin1<Tin2, R:Rb1<Rb2
MR11: r:Tin1>Tin2, R:Rv1>Rv2
MR12: r:Tin1<Tin2, R:Rv1<Rv2
MR13: r:Po1>Po2, R:Pa1>Pa2
MR14: r:Po1<Po2, R:Pa1<Pa2
MR15: r:Po1>Po2, R:Rb1<Rb2
MR16: r:Po1<Po2, R:Rb1>Rb2
MR17: r:Po1>Po2, R:Rv1<Rv2
MR18: r:Po1<Po2, R:Rv1>Rv2
MR19: r:P1>P2, R:To1>To2
MR20: r:P1<P2, R:To1<To2
MR21: r:P1>P2, R:Rb1>Rb2
MR22: r:P1<P2, R:Rb1<Rb2
MR23: r:P1>P2, R:Rv1>Rv2
MR24: r:P1<P2, R:Rv1<Rv2
MR25: r:Lf1>Lf2, R:Vf1<Vf2
MR26: r:Lf1<Lf2, R:Vf1>Vf2
MR27: r:Lf1>Lf2, R:Fps1<Fps2
MR28: r:Lf1<Lf2, R:Fps1>Fps2
MR29: r:Lf1>Lf2, R:To1>To2
MR30: r:Lf1<Lf2, R:To1<To2
MR31: r:Lf1>Lf2, R:Rb1>Rb2
MR32: r:Lf1<Lf2, R:Rb1<Rb2
MR33: r:Lf1>Lf2, R:Rv1>Rv2
MR34: r:Lf1<Lf2, R:Rv1<Rv2
MR35: if Tm1<Tm2 then Vf1<Vf2
MR36: if Tm1<Tm2 then T1<T2
MR37: if Tm1<Tm2 then Rf1<Rf2
MR38: if Tm1<Tm2 then Vf1>Vf2
MR39: if Tm1<Tm2 then T1>T2
MR40: if Tm1<Tm2 then Rf1>Rf2
MR41: r:Kfrom1<Kfrom2, R:Rv1<Rv2
MR42: r:Kfrom1>Kfrom2, R:Rv1>Rv2
MR43: r:Kfrom1<Kfrom2, R:Rb1<Rb2
MR44: r:Kfrom1>Kfrom2, R:Rb1>Rb2
MR45: r:Fps1<Fps2, R:Re1<Re2
MR46: r:Fps1>Fps2, R:Re1>Re2
```
Split: MR1-MR40 expert-identified; MR41-MR46 implicit (newly surfaced).
Note: MR35-MR37 vs MR38-MR40 give opposite output orderings for the same `Tm1<Tm2`
antecedent; transcribed verbatim, flagged for source clarification (the source likely
intends two regimes/conditions). Does not change block classification (still O≤).
