#version 320 es

#ifdef GL_ES
precision mediump float;
#endif

layout(points)in;
layout(points,max_vertices=2)out;

in VS_OUT{
    vec4 geoValue;
}gs_in[];

uniform float additional;

out vec4 outValue;

void main()
{
    for(int i=0;i<2;i++){
        outValue=gs_in[0].geoValue;
        outValue.y += (additional/2.0 - additional * float(i));
        EmitVertex();
        EndPrimitive();
    }
}
