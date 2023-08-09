
def create_visuals(do_screenshot, do_disable_fxaa, do_disable_dynamicres):

    screenshot = "disabled"
    disablefxaa = "disabled"
    disabledynamicres = "disabled"

    do_island = False
    
    visual_fixes = []

    if do_screenshot:
        screenshot = "enabled"
    if do_disable_fxaa:
        disablefxaa = "enabled"
    if do_disable_dynamicres:
        disabledynamicres = "enabled"
        
    visuals1_0_0 = f'''// Screenshot Mode Graphics
@{screenshot}
00A56568 68008052
00A55CD0 1F2003D5
00A55CD4 1F2003D5
@stop

// Disable FXAA
@{disablefxaa}
00B92318 08000014
@stop

// Disable Dynamic Resolution
@{disabledynamicres}
00A583B4 1F2003D5
00A583C8 1F2003D5
@stop
'''

    visuals1_3_0= f'''// Screenshot Mode Graphics
@{screenshot}
005EE238 68008052
005EDB3C 1F2003D5
005EDB40 1F2003D5
@stop

// Disable FXAA
@{disablefxaa}
009BD3A8 08000014
@stop

// Disable Dynamic Resolution
@{disabledynamicres}
005EE438 1F2003D5
@stop
'''

    visual_fixes.append(visuals1_0_0)
    visual_fixes.append(visuals1_3_0)
    
    return visual_fixes