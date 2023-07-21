## Trick to push
- The command `sudo docker push` may error out with this message: `denied: requested access to the resource is denied`.
- On `dockerhub` website, we can create one new repository. It shows a way how to push image to the repository. That is a good example.
- We may tag local image with the format as the above example.
- Then the `docker push` command will work.