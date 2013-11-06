Django S3 Templates
===================

Sometimes you want to load templates from S3.

This is a template loader that you can add to your Django settings.

Still need cacheing at the very least to make this at all production ready, 
but it should work now for asynchronous jobs (like emails). The plan is to 
use the md5 hashes S3 and boto provide to determine changes to the templates
on S3, compile those templates and store them in cache until a change is made 
on S3 or the cache expires.

This would then work for cloud deployments where templates can be deployed
without needing to redeploy. 

Requires Django and Boto, both are brought in if not installed from the setup script.

Needs Tests