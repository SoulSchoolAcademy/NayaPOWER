# OPERATIONS / DEPLOYMENT

Deployment is a boundary, not proof.

## Order
SOURCE -> TEST -> REVIEW -> AUTHORIZED DEPLOY -> RUNTIME VERIFY -> RECORD

A deployment receipt proves deployment occurred. It does not by itself prove production behavior.

If production parity fails, investigate the actual request and runtime contract. Do not weaken acceptance gates to obtain a green result.

Production claims require production evidence.
