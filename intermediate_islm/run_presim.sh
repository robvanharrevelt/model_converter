echo intermediate_islm.inp > presim.inp
echo intermediate_islm.mdl >> presim.inp
echo ISIS OVER >> presim.inp
presim < presim.inp
rm presim.inp
