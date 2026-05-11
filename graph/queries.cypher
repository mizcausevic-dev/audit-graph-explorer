// 1. Find the shortest explanation path from a policy exception to a tier-0 asset.
MATCH p = shortestPath(
  (e:Exception {id: 'exception-233'})-[*..6]-(a:Asset {id: 'asset-admin-console'})
)
RETURN p;

// 2. Show the owner chain for any open exceptions tied to vendor access policy.
MATCH (e:Exception)-[:VIOLATES]->(p:Policy {id: 'policy-vendor-access'})
OPTIONAL MATCH (e)-[:OWNED_BY]->(u:User)-[:MEMBER_OF]->(t:Team)
RETURN e.id AS exception_id, e.name AS exception_name, u.name AS owner, t.name AS team;

// 3. Trace blast radius from a vendor to all downstream assets and incidents.
MATCH (v:Vendor {id: 'vendor-acme'})-[*1..5]-(n)
WHERE n:Asset OR n:Incident OR n:Exception
RETURN DISTINCT labels(n) AS node_labels, n.id AS node_id, n.name AS node_name
ORDER BY node_labels[0], node_id;

// 4. Find all approvals that created or amplified active exception pressure.
MATCH (a:Approval)-[:AFFECTS]->(asset:Asset)<-[:AFFECTS]-(e:Exception)
RETURN a.id, a.name, asset.name, collect(e.id) AS linked_exceptions;

