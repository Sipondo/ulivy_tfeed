"""
Plasma Shader
=============

This shader example have been taken from
http://www.iquilezles.org/apps/shadertoy/ with some adaptation.

This might become a Kivy widget when experimentation will be done.
"""


from kivy.clock import Clock
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.graphics import Mesh, MeshView, RenderContext, BindTexture, Rectangle
from kivy.graphics.texture import Texture
from kivy.core.image import Image, ImageData
from kivy.properties import StringProperty, ObjectProperty
from kivy.core.window import Window
from kivy.resources import resource_find

from kivy.graphics.instructions import TransformFeedback

import numpy as np
import lark
import termcolor
import time

############## TODO: move this to some resource manager thing

with open(resource_find("ulivy_shaders/tfeed_vs.glsl")) as file:
    enti_shader_vs = file.read()

with open(resource_find("ulivy_shaders/tfeed_gs.glsl")) as file:
    enti_shader_gs = file.read()

with open(resource_find("ulivy_shaders/tfeed_fs.glsl")) as file:
    enti_shader_fs = file.read()


with open(resource_find("ulivy_shaders/transform_vs.glsl")) as file:
    transform_vs = file.read()

with open(resource_find("ulivy_shaders/transform_gs.glsl")) as file:
    transform_gs = file.read()

with open(resource_find("ulivy_shaders/transform_fs.glsl")) as file:
    transform_fs = file.read()


#####################


VIEW_WIDTH = 8


class ShaderWidget(FloatLayout):
    def __init__(self, poffset, **kwargs):
        self.canvas = RenderContext(
            fs=enti_shader_fs, gs=enti_shader_gs, vs=enti_shader_vs
        )

        # self.tex1 = Image.load(resource_find("tex4.jpg")).texture
        self.tex2 = Image.load(resource_find("tex2.jpg")).texture

        # self.tex1.mag_filter = "nearest"

        # call the constructor of parent
        # if they are any graphics object, they will be added on our new canvas
        super(ShaderWidget, self).__init__(**kwargs)

        self.poffset = poffset
        self.camera_position = 0

        self.float_x = 0
        self.float_y = 0

        with self.canvas:
            self.mesh = Mesh(
                vertices=[1.0, 1.0, 1.0, 1.0] * 1024,
                indices=[0, 1, 2, 3],
                fmt=[(b"aPos", 2, "float"), (b"aSize", 2, "float"),],
            )
            # self.mesh_clone = MeshView(host_mesh=self.mesh)

        self.canvas.add(BindTexture(texture=self.tex2, index=3,))

        if poffset != -0.25:
            Clock.schedule_interval(self.update, 10 / 60.0)
        else:
            Clock.schedule_once(self.update)

    def update(self, *largs):

        self.float_x += 0.001
        # self.mesh.vertices = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

        # self.mesh.indices = self.mesh.indices

        self.canvas["texture0"] = 3
        self.canvas["poffset"] = float(self.poffset)
        # print("mesh", dir(self.mesh))
        # print(self.mesh_clone)


class ShaderCloneWidget(FloatLayout):
    def __init__(self, poffset, clone, **kwargs):
        self.canvas = RenderContext(
            fs=enti_shader_fs, gs=enti_shader_gs, vs=enti_shader_vs
        )

        # self.tex1 = Image.load(resource_find("tex4.jpg")).texture
        self.tex2 = Image.load(resource_find("tex4.jpg")).texture

        # self.tex1.mag_filter = "nearest"

        # call the constructor of parent
        # if they are any graphics object, they will be added on our new canvas
        super(ShaderCloneWidget, self).__init__(**kwargs)

        self.poffset = poffset
        self.camera_position = 0

        self.float_x = 0
        self.float_y = 0

        with self.canvas:
            # self.mesh = Mesh(
            #     vertices=[0.0, 0.0, 1.0, 1.0],
            #     indices=[0],
            #     fmt=[(b"aPos", 2, "float"), (b"aSize", 2, "float"),],
            # )
            self.mesh_clone = MeshView(host_mesh=clone)

        self.canvas.add(BindTexture(texture=self.tex2, index=2,))
        Clock.schedule_interval(self.update, 1 / 60.0)

    def update(self, *largs):
        self.canvas["texture0"] = 2
        self.canvas["poffset"] = float(self.poffset)
        # print(self.mesh.vertices)
        # print("clone", dir(self.mesh_clone))


class LayoutThing(FloatLayout):
    def __init__(self, **kwargs):
        super(LayoutThing, self).__init__(**kwargs)

        s2 = ShaderWidget(poffset=-0.25)
        self.add_widget(s2)
        sc = ShaderCloneWidget(poffset=0.5, clone=s2.mesh)
        # sc = ShaderWidget(poffset=0.5)  # , clone=s.mesh)
        self.add_widget(sc)

        s = ShaderWidget(poffset=-0.75)
        self.add_widget(s)

        self.s = s
        self.s2 = s2
        self.sc = sc

        self.bla = 1.0

        Clock.schedule_once(self.try_transform, 4)

    def try_transform(self, dt):
        # sc.mesh_clone.transform_geometry_example()

        # self.transformer = TransformFeedback()

        self.transformer = TransformFeedback(
            vs=transform_vs,
            gs=transform_gs,
            fs=transform_fs,
            max_primitives=2,
            in_format=[(b"inVec", 4, "float"),],
        )

        # transformer.transform_geometry_static_example()
        # transformer.transform_static_example()
        # print("PRE:", self.s2.mesh.vertices, self.s2.mesh.indices)

        # print(transformer.transform(self.s.mesh, self.s2.mesh, 4))
        # print("POST:", self.s2.mesh.vertices, self.s2.mesh.indices)
        Clock.schedule_interval(self.do_transform, 1 / 2)
        # Clock.schedule_once(self.do_transform, 1 / 60)
        # Clock.schedule_once(self.do_transform, 121 / 60)

    def do_transform(self, dt):
        # self.transformer = TransformFeedback()

        # print("PRE:", self.s.mesh.vertices, self.s.mesh.indices)
        # print(
        self.transformer["additional"] = 1 / self.bla

        t = time.perf_counter()
        p = self.transformer.transform(
            self.s.mesh, self.s2.mesh, int(self.bla), debug=False
        )
        print(p, "time:", time.perf_counter() - t)
        self.bla *= 2

        self.s, self.s2 = self.s2, self.s
        # )  # , debug=True))
        # print("PRE:", self.s.mesh.vertices, self.s.mesh.indices)
        # print("POST:", self.s2.mesh.vertices, self.s2.mesh.indices, "\n\n\n")


class UlivyApp(App):
    def build(self):
        return LayoutThing()  # fs=plasma_shader)


if __name__ == "__main__":
    UlivyApp().run()

