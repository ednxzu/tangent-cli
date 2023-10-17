# tangent-envs

This tool lets you create a manage test environments using docker to quickly try out things.

## 🤔 What is the use case ?

Well, let's say you are reading up on some new tool that seems very cool, or lets say you Are doing something else entirely, and all of a sudden a wild though crosses your mind: "damn I wonder if <insert any random question> ?". In those scenarios, I used to spin up a docker container using the good-ol ocker cli:

```bash
docker pull ...
docker run -it xxxx bash
```

You know the drill... but it felt too slow, especially since I often needed systemd enabled containers to test out some thing as if I was in a VM.

So I made this, `tangent`, for when I go off on a tangent.

```bash
tangent create -d ubuntu2204 -n haproxy-test -c
```

and off you go ! 🚀

This simply works by pulling the images from [Jeff Geerling's dockerhub repository](https://ansible.jeffgeerling.com/) (for now, I will most likely build specific images later, or add an option to customize the pull target), which are systemd enabled images, and add a label to it so that the tool can identify which images it created or didn't.

It also let's you attach a volume directly to it, that will be created in your homedir, so that you don't have to have access to `/var/lib/docker` in order to copy data to and from the container.

It can then track the running (or stopped) environments you have, and let you reconnect to it, stop it, and destroy it entirely once you're done.

```bash
tangent list
+---------+-----------+------------+--------------------------------+
|  Name   |  Status   | IP Address |            Created             |
+---------+-----------+------------+--------------------------------+
| haproxy | ✔ running | 172.17.0.2 | 2023-10-17T21:06:21.135765924Z |
+---------+-----------+------------+--------------------------------+
```

## 🐍 installation

You can install tangent using pip

```bash
pip3 install git+https://github.com/ednxzu/tangent-cli@<branch-or-tag>
```

> **Warning**
> Tangent is not yet stable enough to make a full on release, so for now, you must use the main branch to install it.

## 🚀 quickstart

The images pulled are from [Jeff Geerling's dockerhub repository](https://ansible.jeffgeerling.com/) (see: Container Images for Ansible Testing). tangent interpolates the distro name to the full image name (`ubuntu2204` pulls `geerlingguy/docker-ubuntu2204-ansible`, etc...)

To create an environment, simply run:

```bash
tangent create -d ubuntu2204 -n test -c
```

`tangent --help` is also available for more details.
