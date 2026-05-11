// Core labels
CREATE CONSTRAINT user_id IF NOT EXISTS FOR (n:User) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT vendor_id IF NOT EXISTS FOR (n:Vendor) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT policy_id IF NOT EXISTS FOR (n:Policy) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT approval_id IF NOT EXISTS FOR (n:Approval) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT incident_id IF NOT EXISTS FOR (n:Incident) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT exception_id IF NOT EXISTS FOR (n:Exception) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT asset_id IF NOT EXISTS FOR (n:Asset) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT region_id IF NOT EXISTS FOR (n:Region) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT environment_id IF NOT EXISTS FOR (n:Environment) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT team_id IF NOT EXISTS FOR (n:Team) REQUIRE n.id IS UNIQUE;

// Lookup indexes
CREATE INDEX policy_severity IF NOT EXISTS FOR (n:Policy) ON (n.severity);
CREATE INDEX exception_status IF NOT EXISTS FOR (n:Exception) ON (n.status);
CREATE INDEX incident_status IF NOT EXISTS FOR (n:Incident) ON (n.status);
CREATE INDEX asset_tier IF NOT EXISTS FOR (n:Asset) ON (n.tier);

