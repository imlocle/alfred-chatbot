terraform {
  backend "s3" {
    bucket       = "alfred-terraform-state-bucket"
    key          = "alfred/dev/terraform.tfstate"
    region       = "us-west-1"
    use_lockfile = true
  }
}
