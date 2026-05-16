from pade_constants import Colors, ArmorLabel, PenLabel, AngleLabel, Shadow
from gambiter import g_guiFlash  # type: ignore
from gambiter.flash import COMPONENT_TYPE, COMPONENT_ALIGN  # type: ignore

ARMOR_ALIAS = "pademinune_ArmorPenLabel"
PROB_ALIAS = "pademinune_ProbabilityLabel"
ANGLE_ALIAS = "pademinune_AngleLabel"


class GuiState:
    is_visible = False
    track_visible = False


def log(message):
    print("pademinune's Gui: " + str(message))


def update_armor_label(armor_value, color):
    interior_label = ArmorLabel.LABEL_FORMAT.format(armor=armor_value)
    new_text = "<font size='{font_size}' color='#{color}' face='$FieldFont'>{label_format}</font>".format(
        font_size=ArmorLabel.FONT_SIZE, color=color, label_format=interior_label
    )

    armor_changes = {"text": new_text, "visible": True}

    if not GuiState.is_visible:
        GuiState.is_visible = True

    g_guiFlash.updateComponent(ARMOR_ALIAS, armor_changes)


def update_prob_label(prob, color):
    interior_label = PenLabel.LABEL_FORMAT.format(prob=prob)
    new_text = "<font size='{font_size}' color='#{color}' face='$FieldFont'>{label_format}</font>".format(
        font_size=PenLabel.FONT_SIZE, color=color, label_format=interior_label
    )

    prob_changes = {"text": new_text, "visible": True}

    if not GuiState.is_visible:
        GuiState.is_visible = True

    g_guiFlash.updateComponent(PROB_ALIAS, prob_changes)


def update_angle_label(angle, color):
    interior_label = AngleLabel.LABEL_FORMAT.format(angle=angle)
    new_text = "<font size='{font_size}' color='#{color}' face='$FieldFont'>{label_format}</font>".format(
        font_size=AngleLabel.FONT_SIZE, color=color, label_format=interior_label
    )
    g_guiFlash.updateComponent(ANGLE_ALIAS, {"text": new_text, "visible": True})


def hide_labels():
    if GuiState.is_visible:
        g_guiFlash.updateComponent(ARMOR_ALIAS, {"visible": False})
        g_guiFlash.updateComponent(PROB_ALIAS, {"visible": False})
        g_guiFlash.updateComponent(ANGLE_ALIAS, {"visible": False})
        GuiState.is_visible = False


def update_gui(armor_value, prob, ricochet, hit_body, hit_track, hit_angle):

    if ricochet:
        # shell ricochet
        color = Colors.PURPLE
        update_armor_label("-", color)
        update_prob_label(0, color)
        update_angle_label(hit_angle, color)
    elif not hit_body:
        # shell only hits spaced armor or tracks
        # color = Colors.RED
        # update_armor_label("-", color)
        # update_prob_label(0, color)
        # g_guiFlash.updateComponent(ANGLE_ALIAS, {"visible": False})
        hide_labels()
    else:
        color = Colors.GREY
        if prob <= 7:
            # armor_val is right of z = 1.5
            color = Colors.RED
        elif prob >= 93:
            # armor_val is left of z = -1.5
            color = Colors.GREEN
        else:
            color = Colors.ORANGE

        update_armor_label(int(armor_value), color)
        update_prob_label(int(prob), color)
        update_angle_label(hit_angle, color)


log("Starting creation of armor and penetration gui components")


def _build_glowfilter():
    return {
        "color": int(Shadow.COLOR, 16),
        "alpha": Shadow.ALPHA / 10.0,
        "blurX": Shadow.LENGTH,
        "blurY": Shadow.LENGTH,
        "strength": Shadow.STRENGTH,
        "quality": 2,
    }


armor_label_properties = {
    "isHtml": True,
    "text": "",
    "glowfilter": _build_glowfilter(),
    "alignX": COMPONENT_ALIGN.CENTER,
    "alignY": COMPONENT_ALIGN.CENTER,
    "x": ArmorLabel.X_OFFSET,
    "y": ArmorLabel.Y_OFFSET,
    "visible": False,
}

probability_label_properties = {
    "isHtml": True,
    "text": "",
    "glowfilter": _build_glowfilter(),
    "alignX": COMPONENT_ALIGN.CENTER,
    "alignY": COMPONENT_ALIGN.CENTER,
    "x": PenLabel.X_OFFSET,
    "y": PenLabel.Y_OFFSET,
    "visible": False,
}

angle_label_properties = {
    "isHtml": True,
    "text": "",
    "glowfilter": _build_glowfilter(),
    "alignX": COMPONENT_ALIGN.CENTER,
    "alignY": COMPONENT_ALIGN.CENTER,
    "x": AngleLabel.X_OFFSET,
    "y": AngleLabel.Y_OFFSET,
    "visible": False,
}

# create the armor value label
g_guiFlash.createComponent(ARMOR_ALIAS, COMPONENT_TYPE.LABEL, armor_label_properties)
# create the probability label
g_guiFlash.createComponent(PROB_ALIAS, COMPONENT_TYPE.LABEL, probability_label_properties)
# create the angle label
g_guiFlash.createComponent(ANGLE_ALIAS, COMPONENT_TYPE.LABEL, angle_label_properties)


def update_label_properties():
    glowfilter = _build_glowfilter()
    g_guiFlash.updateComponent(
        ARMOR_ALIAS,
        {
            "x": ArmorLabel.X_OFFSET,
            "y": ArmorLabel.Y_OFFSET,
            "glowfilter": glowfilter,
        },
    )
    g_guiFlash.updateComponent(
        PROB_ALIAS,
        {
            "x": PenLabel.X_OFFSET,
            "y": PenLabel.Y_OFFSET,
            "glowfilter": glowfilter,
        },
    )
    g_guiFlash.updateComponent(
        ANGLE_ALIAS,
        {
            "x": AngleLabel.X_OFFSET,
            "y": AngleLabel.Y_OFFSET,
            "glowfilter": glowfilter,
        },
    )


log("GUI components have been created!")
