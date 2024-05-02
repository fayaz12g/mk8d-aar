def create_visuals(do_split60, do_disabledynamic, do_nosteer, do_dofscaler, do_fxaaoff, do_fxaaon, do_fxaaonscaler, do_lodenhance):

    split60 = "disabled"
    dynamic = "disabled"
    nosteer = "disabled"
    dofscaler = "disabled"
    fxaaoff = "disabled"
    fxaaon = "disabled"
    fxaaonscaler = "disabled"
    lodenhance = "disabled"

    visual_fixes = []

    do_split60 = eval(do_split60)
    do_disabledynamic = eval(do_disabledynamic)
    
    if do_split60:
        split60 = "enabled"
    if do_disabledynamic:
        dynamic = "enabled"
    if do_nosteer:
        nosteer = "enabled"
    if do_dofscaler:
        dofscaler = "enabled"
    if do_fxaaoff:
        fxaaoff = "enabled"
    if do_fxaaon:
        fxaaon = "enabled"
    if do_fxaaonscaler:
        fxaaonscaler = "enabled"
    if do_lodenhance:
        lodenhance = "enabled"
        
    visuals3_0_1 = f'''// 60 FPS in Splitscreen
@{split60}
00BC0B3C 970000EA
@disabled

// Dynamic Res Disable
@{dynamic}
0079DD84 9D0200EA
@disabled

// Disable Steer Assist
@{nosteer}
0018B764 0000A0E3
@disabled

// DOF Scaler Fix
@{dofscaler}
00B81630 003AB7EE
@disabled

// Force FXAA Off
@{fxaaoff}
006B54F4 00F020E3
@disabled

// Force FXAA On
@{fxaaon}
006B590C 00F020E3
@disabled

// Force FXAA On - Scaler Fix
@{fxaaonscaler}
006B56F8 3F94A0E3
006B590C 00F020E3
@disabled

// LOD Enhancement
@{lodenhance}
0088ED3C 0020A0E3
006F051C 001AB0EE
00AF41C4 000AB9EE
00B1EB34 000ABBEE
@stop
'''
    visual_fixes.append(visuals3_0_1)
    
    return visual_fixes