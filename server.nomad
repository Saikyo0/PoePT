job "poe-server" {
  group "group-1" {
    task "api-server" {
      driver = "docker"

      # https://developer.hashicorp.com/nomad/docs/drivers/docker
      config {
        image      = "${IMAGE_TAG}"
        force_pull = true
        ports      = ["http"]
        args       = ["python3", "-m", "poept.server", "--hostname", "0.0.0.0", "--port", "${NOMAD_PORT_http}"]
      }

      env {
        POE_COOKIES     = "${POE_COOKIES}"
        POE_AUTH_TOKENS = "${POE_AUTH_TOKENS}"
      }
    }

    # Setup port mapping here
    # https://developer.hashicorp.com/nomad/docs/drivers/docker#using-the-port-map
    network {
      port "http" { static = 8080 }
      mode = "host"
    }
  }
}
