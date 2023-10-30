# Introduction to data science mini project

This is a mini project developed in part of the Introduction to data science course at University of Helsinki.

The aim of the project is to create an app for people, who are considering to buy a new game for a decent price on [Steam](https://store.steampowered.com/).

# Run with docker

At first, clone this repository.

Build a docker image in the root directory

`docker build . -t gamesaver`

Run with the command

`docker run -p 8080:8080 -t gamesaver`
