sfflag=true
local c = addChannel("Camera", 1, 0, 0, 2)
lastResponse = getUptime()
lastKeepAlive = getUptime()
lastRequest = getUptime()

function sendRaw(val)
    for i = 1, #val do
        local c = string.sub(val, i, i)
        writeCSer(5, string.byte(c))
    end
end

function sendAt(val)
    sendRaw(val)
    writeCSer(5, 13)
    writeCSer(5, 10)
end

function sendCommand(command, connection)
    sendAt('AT+CIPSEND=' .. connection .. ',' .. string.sub(#command, 1, -3))
    pi()
    sendRaw(command)
    pi()
end

function pi() -- process incoming, reads from serial character by character
    local char = readCSer(5, 100)
    if char == nil then
        return
    end
    local line = ''
    while (char ~= nil) do
        line = line .. string.char(char)
        if string.find(line, '+IPD,') then -- This means incoming packet
            readCSer(5, 100)
            char = readCSer(5, 100)
            char = readCSer(5, 100)
            local length = ''
            while char ~= 58 do
                if char == nil then
                    return
                end
                length = length .. string.char(char)
                char = readCSer(5, 100)
            end
            local packet = ''
            if tonumber(length) == nil then
            else
                for i = 1, tonumber(length) do
                    packet = packet .. string.sub(readCSer(5, 100), 1, -3) .. ' '
                end
                lastResponse = getUptime()
                if getChannel(c) == 0 then
                    setChannel(c, 1)
                end
                if packet == '95 71 80 72 68 95 58 48 58 48 58 50 58 1 ' then -- This is the KeepAlive response
                    if getChannel(c) == 0 then
                        setChannel(c, 1)
                    end
                elseif packet == '0 0 0 0 0 0 0 0 0 0 0 115 116 0 0 0 0 0 0 0 ' then -- This response means camera is on and not recording
                    setChannel(c, 1)
                elseif packet == '0 0 0 0 0 0 0 0 0 0 0 115 116 0 0 1 0 1 0 0 ' then -- This response means the camera IS recording
                    setChannel(c, 2)
                elseif packet == '0 0 0 0 0 0 0 0 0 0 0 115 116 1 0 0 0 0 0 0 ' then -- This means the camera is off
                    setChannel(c, 0)
                end
                return
            end
        end
        char = readCSer(5, 100)
    end
end

sendAt('AT+RST') -- Reset ESP8266
pi()
sendAt('AT+CWMODE_CUR=2') -- Set as an access point
pi()
sendAt('AT+CWSAP_CUR="HERO-RC-000071","",1,0') -- This is the SSID to emulate a remote.  The last 6 need to match the below piece
pi()
sendAt('AT+CIPAPMAC_CUR="d8:96:85:00:00:71"') -- Remote MAC address all start with the same 3 sets, then you can use any set.  all 0's work
pi()
sendAt('AT+CIPAP_CUR="10.71.79.1"') -- The remote IP
pi()
sendAt('AT+CIPMUX=1') -- Setting to accept multiple connections
pi()
sleep(1000)
sendAt('AT+CIPSTART=0,"UDP","255.255.255.255",9') -- Set up a connection to the subnet for the WOL
pi()
sendAt('AT+CIPSTART=1,"UDP","10.71.79.2",8484,8383') -- Set up a connection to the camera
pi()

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
    -- checkCamera()
    if (getUptime() - lastResponse) > 5000 then -- If there has been no response for 5 seconds, start sending a WOL packet
        setChannel(c, 0) -- Set camera to not connected
        local mac = string.char(0xd4, 0xd9, 0x19, 0xd2, 0x95, 0xdd) -- This is the mac addres of my camera, d4:d9:19:d2:95:dd
        local packet = string.char(0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF) -- The opening of the packet is a null packet
        for i = 1, 16 do
            packet = packet .. mac -- And then the MAC address 16 times
        end
        sendCommand(packet, '0')
    end
    if isLogging() == 0 and getChannel(c) == 2 then -- If we are not logging, but the camera is recording, stop the camera
     sendCommand(string.char(0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x53, 0x48, 0x00), '1') -- Stop camera
        setChannel(c, 1)
    end
    if isLogging() ~= 0 and getChannel(c) == 1 then -- If we ARE logging, and not recording, then record
        sendCommand(string.char(0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x53, 0x48, 0x02), '1') -- Start camera
        setChannel(c, 2)
    end
    if (getUptime() - lastKeepAlive) > 1500 then -- Send a keep alive packet every 1.5 seconds
        sendAt('AT+CIPSEND=1,22')
        pi()
        sendRaw('_GPHD_:0:0:2:0.000000\n') -- This is the actual keep alive command
        pi()
        lastKeepAlive = getUptime()
    end
    if (getUptime() - lastRequest) > 5000 then -- Send a status request every 5 seonds
        sendCommand(string.char(0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x73, 0x74), '1') -- This is the actual request command
        lastRequest = getUptime()
    end
    pi() -- Process incoming every tick
end
