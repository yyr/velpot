; Copyright (C) Yagnesh Raghava Yakkala. http://yagnesh.org
; Created: Tuesday, July 17 2018

begin
  fname = "fnl_20090801_00_00.grib2"
  fh = addfile(fname, "r")
  oh = addfile("sf_vp.nc", "c")

  u = fh->UGRD_P0_L6_GLL0
  v = fh->VGRD_P0_L6_GLL0

  uvmsg = 1e+36

  sf = new(dimsizes(u), float, uvmsg)
  vp = new(dimsizes(v),float, uvmsg)

  ; printVarSummary(u)
  ; printVarSummary(vp)

  uv2sfvpf (u,v, sf,vp)
  ; printMinMax(sf,True)
  ; printMinMax(vp,True)

  oh->SF = sf
  oh->VP = vp
end
