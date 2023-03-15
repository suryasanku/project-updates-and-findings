    # mongo 
      show dbs
      use vitalsDB
      db.getCollectionNames();

================================================================

    # db.patientsVitals.find({"hubMacId":"10:ae:7b:64:0b:7a"}).pretty()


=================================================================

    # db.alarms.find({"hubMacId":"10:ae:7b:64:0b:7a"}).pretty()


=================================================================

    # db.alarms.find();
     db.alarms.find().pretty();
     db.alarms.find({"hubMacId":"10:ae:7b:64:0b:7a"}).pretty()

=================================================================

    # db.alarms.find({"hubMacId":"10:ae:7b:64:0b:7a"}).sort({ createdTime: 1 }).pretty() -->assending 
    # db.alarms.find({"hubMacId":"10:ae:7b:64:0b:7a"}).sort({ createdTime:-1 }).pretty()--> descending (-1)

============================================================

    # db.vitalsLegends.update({"_id" : ObjectId("62ea4f598bc6373401ab5009")},{$set:{"deviceType" : "blood_pressure"}})

================================================================

    # db.patientsVitals.deleteMany( { "deviceType" : "${deviceType}" } );

