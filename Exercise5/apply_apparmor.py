
import docker

client = docker.from_env()

IMAGE = "flask-apparmor"
PROFILE = "my-apparmor-profile"
CONTAINER_NAME = "flask-apparmor-sdk"

# Build the image
client.images.build(path=".", tag=IMAGE)
print("Image built successfully.")

# Check whether Docker reports AppArmor support
info = client.info()
print("Docker security options:", info.get("SecurityOptions", []))

# Run with the requested AppArmor profile
try:
    container = client.containers.run(
        IMAGE,
        name=CONTAINER_NAME,
        ports={"5000/tcp": 5001},
        security_opt=[f"apparmor={PROFILE}"],
        detach=True,
    )

    print("Container started:", container.short_id)

    details = client.api.inspect_container(container.id)
    print("Configured security options:",
          details["HostConfig"].get("SecurityOpt"))

    print("Reported AppArmor profile:",
          details.get("AppArmorProfile"))

except docker.errors.APIError as exc:
    print("Docker could not start the container with this profile.")
    print(exc)

finally:
    existing = client.containers.get(CONTAINER_NAME) \
        if any(c.name == CONTAINER_NAME
               for c in client.containers.list(all=True)) else None

    if existing:
        existing.remove(force=True)
        print("Test container removed.")
