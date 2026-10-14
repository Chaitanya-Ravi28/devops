import docker

client = docker.from_env()

IMAGE = "flask-apparmor"
PROFILE = "my-apparmor-profile"
CONTAINER_NAME = "flask-apparmor-restriction-test"

container = None

try:
    container = client.containers.run(
        IMAGE,
        name=CONTAINER_NAME,
        security_opt=[f"apparmor={PROFILE}"],
        detach=True,
    )

    print("Container started:", container.short_id)

    # Test reading a sensitive file
    exit_code, output = container.exec_run(
        ["cat", "/etc/passwd"]
    )
    print("Read /etc/passwd:")
    print("Exit code:", exit_code)
    print(output.decode(errors="replace"))

    # Test executing a shell
    exit_code, output = container.exec_run(
        ["/bin/bash", "-c", "echo shell-executed"]
    )
    print("Execute /bin/bash:")
    print("Exit code:", exit_code)
    print(output.decode(errors="replace"))

finally:
    if container is not None:
        container.remove(force=True)
        print("Test container removed.")
