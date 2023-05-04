# AWS-Athena-Log-Analysis

Script to use csvq command for csv log file of Athena:
```
SELECT useridentity,eventtime,eventname,awsregion,sourceipaddress,useragent,errorcode,errormessage,requestparameters,resources,eventtype,recipientaccountid,vpcendpointid,account_id,region
FROM cloudtraildb.cloudtraillogs
WHERE
eventsource = 's3.amazonaws.com' AND
eventname in ('PutObject','GetObject','DeleteObject','HeadObject','PostObject') AND
(errorcode = 'AccessDenied' OR errormessage = 'AccessDenied') AND
parse_datetime(eventtime,'yyyy-MM-dd''T''HH:mm:ss''Z')
BETWEEN parse_datetime('2023-04-20T00:00:00Z','yyyy-MM-dd''T''HH:mm:ss''Z')
AND
parse_datetime('2023-05-04T11:00:00Z','yyyy-MM-dd''T''HH:mm:ss''Z')
ORDER BY eventtime DESC;

==> Download csv file and analyse 

cat <name_file>.csv | csvq -o analysis-result.csv 'select count(*), DATETIME_FORMAT(eventtime, "%Y-%m-%d") as Date, useridentity as UserIdentity, eventname as Method, JSON_VALUE("bucketName", requestparameters) as BucketName, JSON_VALUE("key", requestparameters) as Key from stdin where account_id = "<id>" and recipientaccountid = "<id>" group by eventtime, useridentity, eventname, requestparameters'
```
