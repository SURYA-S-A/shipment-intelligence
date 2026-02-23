# Mock incoming communication events to trigger the agent workflow

# SHP1001 — NYC → Miami | FastTrack Logistics

## Email from Carrier
{
  "channel": "email",
  "source": "dispatch@fasttracklogistics.com",
  "content": "Subject: Delay Update – Shipment SHP1001\n\nDear Operations Team,\n\nShipment SHP1001 from New York to Miami has been delayed due to heavy rain near Philadelphia, PA. The driver has been advised to hold until conditions improve.\n\nRevised ETA is 10:00 PM today.\n\nRegards,\nMichael Ross\nDispatch Manager\nFastTrack Logistics",
  "timestamp": "2026-02-20T11:00:00"
}

## Email from Customer
{
  "channel": "email",
  "source": "ops@acmecorp.com",
  "content": "Subject: Urgent – SHP1001 Not Arrived\n\nHello,\n\nWe were expecting shipment SHP1001 at our Miami warehouse by 4:00 PM. It has not arrived.\n\nThis contains critical production materials needed tomorrow morning. Please confirm ETA.\n\nRegards,\nJohn Doe\nAcme Corp",
  "timestamp": "2026-02-20T16:30:00"
}

## SMS
{
  "channel": "sms",
  "source": "+15551234567",
  "content": "SHP1001 delayed near Philadelphia due to rain. New ETA 10 PM. - FastTrack Logistics",
  "timestamp": "2026-02-20T11:05:00"
}

---

# SHP1002 — Chicago → Dallas | SwiftShip Co

## Email from Carrier
{
  "channel": "email",
  "source": "ops@swiftship.com",
  "content": "Subject: Delay Notice – SHP1002\n\nDear Team,\n\nShipment SHP1002 traveling from Chicago to Dallas has encountered severe wind conditions near Oklahoma City. The driver has pulled over for safety.\n\nUpdated ETA is 2:00 PM today.\n\nSwiftShip Operations",
  "timestamp": "2026-02-21T08:30:00"
}

## Call Transcript
{
  "channel": "call",
  "source": "+15559876543",
  "content": "Agent: Thank you for calling shipment support. How can I help?\n\nCustomer: This is Sarah from Global Traders. Our shipment SHP1002 from Chicago was supposed to arrive in Dallas by 10 AM. It's almost noon and nothing.\n\nAgent: I can see SHP1002 is delayed near Oklahoma City due to high winds.\n\nCustomer: We have a client delivery scheduled this afternoon. Please escalate this immediately.\n\nAgent: Understood, escalating now and will keep you updated.",
  "timestamp": "2026-02-21T11:45:00"
}

---

# SHP1003 — Seattle → Denver | PacificRoute Freight

## Email from Carrier
{
  "channel": "email",
  "source": "dispatch@pacificroute.com",
  "content": "Subject: SHP1003 Delay – Weather Advisory\n\nHello,\n\nShipment SHP1003 from Seattle to Denver is delayed due to blizzard conditions near Salt Lake City. The route has been temporarily closed by state authorities.\n\nRevised ETA is 3:00 PM today.\n\nPacificRoute Freight",
  "timestamp": "2026-02-18T07:00:00"
}

## SMS
{
  "channel": "sms",
  "source": "+15553456789",
  "content": "SHP1003 held near Salt Lake City due to blizzard. ETA updated to 3 PM. - PacificRoute",
  "timestamp": "2026-02-18T07:10:00"
}

## Email from Customer
{
  "channel": "email",
  "source": "warehouse@pacifictech.com",
  "content": "Subject: SHP1003 – Where is our shipment?\n\nHi,\n\nOur shipment SHP1003 from Seattle was expected at our Denver facility at 9 AM. No update received.\n\nWe need this urgently for a client project. Please advise.\n\nPacificTech Supplies",
  "timestamp": "2026-02-18T10:00:00"
}

---

# SHP1004 — Atlanta → Boston | EastCoast Logistics

## Email from Carrier
{
  "channel": "email",
  "source": "support@eastcoastlogistics.com",
  "content": "Subject: Minor Delay – SHP1004\n\nDear Team,\n\nShipment SHP1004 from Atlanta to Boston is experiencing a minor delay due to thunderstorms near Richmond, VA.\n\nWe expect arrival by 6:00 PM today instead of 12:00 PM.\n\nEastCoast Logistics",
  "timestamp": "2026-02-22T09:00:00"
}

## Call Transcript
{
  "channel": "call",
  "source": "+15556543210",
  "content": "Agent: Shipment support, how can I help?\n\nCustomer: Hi, this is Mark from NorthEast Manufacturing. SHP1004 was due this morning from Atlanta. Still nothing.\n\nAgent: I see SHP1004 is delayed near Richmond due to thunderstorms. ETA is now 6 PM.\n\nCustomer: That's a 6 hour delay. We need someone to coordinate with our receiving team.\n\nAgent: I'll make sure the team is notified and updated.",
  "timestamp": "2026-02-22T13:00:00"
}

---

# SHP1005 — Houston → Phoenix | SunBelt Carriers

## Email from Carrier
{
  "channel": "email",
  "source": "dispatch@sunbeltcarriers.com",
  "content": "Subject: SHP1005 Delay – Severe Thunderstorm\n\nHello,\n\nShipment SHP1005 from Houston to Phoenix has been significantly delayed due to a severe thunderstorm system over Houston. The driver is currently waiting at a rest stop.\n\nNew ETA is 4:00 PM today.\n\nSunBelt Carriers",
  "timestamp": "2026-02-21T06:00:00"
}

## SMS
{
  "channel": "sms",
  "source": "+15557891234",
  "content": "SHP1005 delayed in Houston due to thunderstorm. New ETA 4 PM. - SunBelt Carriers",
  "timestamp": "2026-02-21T06:05:00"
}

## Email from Customer
{
  "channel": "email",
  "source": "ops@sunstate.com",
  "content": "Subject: SHP1005 Critical Delay\n\nHi,\n\nSHP1005 was scheduled to arrive in Phoenix at 8 AM. It is now past noon with no delivery.\n\nThis shipment contains temperature-sensitive materials. Please confirm status immediately and escalate if needed.\n\nSunState Industries",
  "timestamp": "2026-02-21T12:30:00"
}

---

# SHP1006 — Minneapolis → Kansas City | MidWest Express

## Email from Carrier
{
  "channel": "email",
  "source": "ops@midwestexpress.com",
  "content": "Subject: SHP1006 Blizzard Delay\n\nDear Operations,\n\nShipment SHP1006 from Minneapolis to Kansas City is delayed due to blizzard conditions near Minneapolis. Roads are closed and the driver is waiting at depot.\n\nRevised ETA is 8:00 PM today.\n\nMidWest Express",
  "timestamp": "2026-02-20T08:00:00"
}

## Call Transcript
{
  "channel": "call",
  "source": "+15552345678",
  "content": "Agent: Shipment support, how may I help?\n\nCustomer: This is Tom from MidWest Distributors. Our shipment SHP1006 from Minneapolis hasn't moved since this morning.\n\nAgent: Yes, SHP1006 is held due to a blizzard near Minneapolis. ETA is now 8 PM.\n\nCustomer: That's a 6 hour delay. We have retail clients waiting. Please mark this urgent and send updates every 2 hours.\n\nAgent: Absolutely, escalating now and scheduling regular updates.",
  "timestamp": "2026-02-20T14:00:00"
}

## SMS
{
  "channel": "sms",
  "source": "+15552345678",
  "content": "SHP1006 stuck in blizzard near Minneapolis. ETA now 8 PM. - MidWest Express",
  "timestamp": "2026-02-20T08:10:00"
}

---

# SHP1009 — NYC → Miami | FastTrack Logistics

## Email from Carrier
{
  "channel": "email",
  "source": "dispatch@fasttracklogistics.com",
  "content": "Subject: Delay Update – Shipment SHP1009\n\nDear Operations Team,\n\nShipment SHP1009 from New York to Miami has been delayed due to severe weather conditions near Chicago, IL. The truck was temporarily halted for safety reasons.\n\nRevised ETA is 10:00 PM tonight.\n\nMichael Ross\nFastTrack Logistics",
  "timestamp": "2026-02-19T10:40:00"
}

## Email from Customer
{
  "channel": "email",
  "source": "john.doe@acmecorp.com",
  "content": "Subject: Urgent – Shipment SHP1009 Delayed\n\nHello,\n\nWe were expecting SHP1009 at our Miami warehouse today by 4:00 PM. This shipment contains critical materials for tomorrow's production.\n\nPlease confirm updated ETA.\n\nJohn Doe\nAcme Corp",
  "timestamp": "2026-02-19T10:50:00"
}

## Call Transcript
{
  "channel": "call",
  "source": "+15551234567",
  "content": "Agent: Shipment support. How can I help?\n\nCustomer: Hi, this is John from Acme Corp regarding SHP1009. It hasn't arrived at our Miami warehouse.\n\nAgent: SHP1009 is delayed near Chicago due to weather.\n\nCustomer: This is critical for our production line tomorrow. Please escalate and notify us of any updates.\n\nAgent: Understood, escalating now.",
  "timestamp": "2026-02-19T10:55:00"
}

## SMS
{
  "channel": "sms",
  "source": "+15559876543",
  "content": "Update: SHP1009 delayed near Chicago due to storm. New ETA 10 PM. - FastTrack Logistics",
  "timestamp": "2026-02-19T10:42:00"
}