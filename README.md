This is just a demo implementation of a very simple problem.  As expected, I had to cut quite a few corners to get it done in reasonable time.

Corners cut:
1. No testing. -- Due to time constraints, there are no unit or integration tests.  This makes me feel bad.  Please do not do this in real life.
2. No CD pipeline -- I rely on `bin/build_and_push.sh` script to push the Docker image to the private container image registry.
3. Very sparse Terraform config -- it only specifies bits of the infrastructure that generate the expense for me (ECS cluster & load balancer).  There is a lot of configuration I've done via AWS UI (e.g. ECS tasks) that should really be part of the Terraform.  (The reason why I have Terraform at all is so I can destroy all the infra when the project is over)
4. Postgres in container -- although the database I'm using is the proper one (Postgres), it is deployed as a transient container. Therefore, all the data is wiped out when I am updating the service. This is obviously bad. (But I couldn't really justify time expense of setting up that thing properly too, sorry).
5. No real frontend -- I am generating static HTML pages, not using any fancy JS.

.... Probably bunch of other stuff.