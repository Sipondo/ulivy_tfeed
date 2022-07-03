#version 320 es

#ifdef GL_ES
precision mediump float;
#endif

in vec4 inVec;

out VS_OUT{
    vec4 geoValue;
}vs_out;

void main()
{
    vs_out.geoValue=inVec;
}
