.PHONY: image video

image:
	docker build -t manim-flexibletextmesh .

video:
	docker run --rm -it --user="$(id -u):$(id -g)" -v ./src:/manim manim-flexibletextmesh manim main.py FlexibleTextMesh -qm \
	&& mkdir -p video \
	&& cp ./src/media/videos/main/720p30/FlexibleTextMesh.mp4 ./video
