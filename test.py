from flask import Flask, jsonify, render_template, request

from papibotapp.grandpy import GrandPy

grandpy = GrandPy("")
test = grandpy.grandpyTalk()

appen = True
