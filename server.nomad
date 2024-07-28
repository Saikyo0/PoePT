job "poe-server" {
  group "group-1" {
    task "http-server" {
      driver = "docker"

      # https://developer.hashicorp.com/nomad/docs/drivers/docker
      config {
        image      = "${IMAGE_TAG}"
        args       = ["python3", "-m", "poept.server"]
        force_pull = true
      }

      env {
        POE_COOKIES = "${POE_COOKIES}"
      }
    }
  }
}
