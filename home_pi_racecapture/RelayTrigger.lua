sfflag=true
setTickRate(30)
function onTick()
 sf = getAtStartFinish()
 if  sf ~= sfflag then
  sfflag = sf
  if sf then
   println( "start finish detected" )
   txCAN(1, 5, 0, {1,2,3,4,5,6,7,8})
  else
   println( "not in start finish zone" )
  end
 end
end