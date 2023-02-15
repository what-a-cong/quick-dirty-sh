#RUN: python %s | filecheck %s

print("Hello world!")
# CHECK: Hello world!
