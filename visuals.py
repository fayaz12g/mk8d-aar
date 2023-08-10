
def create_visuals(do_steering, do_disable_fxaa, do_disable_dynamicres, do_disabledof, do_lodimprove, do_fpssplit):

    steering = "disabled"
    disablefxaa = "disabled"
    disabledynamicres = "disabled"
    disabledof = "disabled"
    lodimprove = "disabled"
    fpssplit = "disabled"
    
    visual_fixes = []

    do_steering = eval(do_steering)
    do_disable_fxaa = eval(do_disable_fxaa)
    do_disable_dynamicres = eval(do_disable_dynamicres)
    do_disabledof = eval(do_disabledof)
    do_lodimprove = eval(do_lodimprove)
    do_fpssplit = eval(do_fpssplit)
    
    if do_steering:
        steering = "enabled"
    if do_disable_fxaa:
        disablefxaa = "enabled"
    if do_disable_dynamicres:
        disabledynamicres = "enabled"
    if do_disabledof:
        disabledof = "enabled"
    if do_lodimprove:
        lodimprove = "enabled"
    if do_fpssplit:
        fpssplit = "enabled"
        
    visuals1_0_0 = f'''// Screenshot Mode Graphics
@{steering}
00A56568 68008052
00A55CD0 1F2003D5
00A55CD4 1F2003D5
@stop

// Disable FXAA
@{disablefxaa}
00B92318 08000014
@stop

// Disable Steering Assist
@enabled
0012ad4c 820000EA
@stop

// Disable Dynamic Resolution
@{disabledynamicres}
00A583B4 1F2003D5
00A583C8 1F2003D5
@stop
'''

    visuals2_4_0= f'''// Lod Improvement
@{lodimprove}
00851978 0020A0E3
006b304c 001AB0EE
@stop

// Disable Steering Assist
@{steering}
0012ad4c 820000EA
@stop

// Double DOF Resolution
@{disabledof}
00b42230 003AB7EE
@stop

// Disable FXAA
@{disablefxaa}
00678024 00F020E3
@stop

// Disable Dynamic Resolution
@{disabledynamicres}
007608b4 9D0200EA
@stop

// 60 FPS In Splitscreen
@{fpssplit}
00b8173c 970000EA
@stop
'''

    visual_fixes.append(visuals1_0_0)
    visual_fixes.append(visuals2_4_0)
    
    return visual_fixes