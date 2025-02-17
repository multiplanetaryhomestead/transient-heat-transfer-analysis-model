#!/usr/bin/env python
#
# Example transient conductive heat transfer analysis
# for a thermocouple measurement of a gas stream
# using lumped capacitance method.
#
# References:
# - Fundamentals of Heat and Mass Transfer, 6e, p.261-263
#

from math import pi, log
from pint import UnitRegistry

u = UnitRegistry(autoconvert_offset_to_baseunit = True)

## Parameters
T_inf = 200 * u('degrees C')
T_i = 25 * u('degrees C')
Tf = 199 * u('degrees C')
τ_t = 1 * u('seconds')

## Constants

### thermal conductivity of thermocouple junction
k = 20 * u('watt')/(u('meter kelvin'))

### specific heat of thermocouple junction
c = 400 * u('joule')/(u('kilogram kelvin'))

### density of thermocouple junction
ρ = 8500 * u('kilogram')/u('cubic meter') 

### convection coefficient
h = 400 * u('watt')/(u('square meter kelvin'))

## Analysis

### required thermojunction diameter needed to reach 1s thermal time constant
D = 6 * h * τ_t / ( ρ * c )
D.ito('millimeters')
r = D / 2
L = r / 3
Bi = h * L / k
Bi.ito('dimensionless')

### Solve for 
t = -τ_t * log((Tf - T_inf) / (T_i - T_inf))
t.ito('seconds')

problem_statement = f"""
A thermocouple junction is used for temperature measurement in a gas stream. Determine 1) The junction diameter needed for the thermocouple to have a time constant of 1 second 2) How long it will take for the junction to reach {round(Tf, 3)} If the junction is at {round(T_i, 3)} and placed in a gas stream that is at {round(T_inf, 3)}.
"""

schematic = f"""
    T_i = {T_i}
    k = {k}
    c = {c}
    p = {ρ}
           ---------- 
          /          \\          T_inf = {T_inf}
         /            \\         h = {round(h, 3)}
        / Thermocouple \\            <----
        \\   junction   /            <----
         \\            /         ( gas stream )
          \\          /
           ----------

"""

assumptions = """
1. Temperature of junction is uniform at any instant
2. Radiation exchange with the surroundings is negligible
3. Losses by conduction through the leads are negligible
4. Constant properties
"""

analysis = f"""
Solving for required thermocouple junction diameter;
D = 6 * h * τ_t / ( ρ * c ) = {round(D, 5)}

Validity of lumped capacitance method:
L = D / 3 = {round(L,3)}
Bi = h * L / k = {round(Bi, 5)}

Comment: Lumped capacitance model is valid for Bi < 0.1

time equation for lumped capacitance model:
t = -τ0 * log((Tf - T_inf) / (T_i - T_inf)) = {round(t, 1)}
"""

solution = f"""
t
"""

print("== Problem Statement ==")
print(problem_statement)
print("== Schematic ==")
print(schematic)
print("== Analysis ==")
print(analysis)

