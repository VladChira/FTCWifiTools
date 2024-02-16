from __future__ import absolute_import

from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from imgui.integrations.pygame import PygameRenderer
import OpenGL.GL as gl
import imgui
import pygame
import sys

from teams.team_manager import TeamManager
from utils import *
from airodump.airodump_manager import *
from tshark.tshark_manager import *

def team1UI():
    imgui.text("Select Red Alliance Team 1")
    imgui.push_item_width(150)
    # imgui.internal.push_item_flag(imgui.SELECTABLE_DISABLED, True)

    if imgui.begin_combo("##Dropdown1", TeamManager().teams[TeamManager().RedTeam1.dropdownTeamNumber]):
        for i, item in enumerate(TeamManager().teams):
                is_selected = (i == TeamManager().RedTeam1.dropdownTeamNumber)
                if imgui.selectable(item, is_selected)[0] is True:
                    TeamManager().RedTeam1.dropdownTeamNumber = i
                if is_selected:
                    imgui.set_item_default_focus()
        imgui.end_combo()

    imgui.pop_item_width()
    # imgui.internal.pop_item_flag()
    imgui.same_line()

    if "Auto" in TeamManager().RedTeam1.status_message:
        imgui.push_style_color(imgui.COLOR_TEXT, 0.0, 1.0, 0.0, 1.0)
    else:
        imgui.push_style_color(imgui.COLOR_TEXT, 1.0, 0.75, 0.0, 1.0)

    imgui.text_unformatted(TeamManager().RedTeam1.status_message)
    imgui.pop_style_color()

    imgui.dummy(0.0, 50.0)
    imgui.same_line()
    _, TeamManager().RedTeam1.overriden = imgui.checkbox("Manual channel override##R1", TeamManager().RedTeam1.overriden)

    if TeamManager().RedTeam1.overriden:
        imgui.same_line()
        imgui.push_item_width(100)
        _, TeamManager().RedTeam1.override_text = imgui.input_text("##R1Textbox", TeamManager().RedTeam1.override_text, 50)
        imgui.pop_item_width()

def team2UI():
    imgui.text("Select Red Alliance Team 2")
    imgui.push_item_width(150)
    # imgui.internal.push_item_flag(imgui.SELECTABLE_DISABLED, True)

    if imgui.begin_combo("##Dropdown2", TeamManager().teams[TeamManager().RedTeam2.dropdownTeamNumber]):
        for i, item in enumerate(TeamManager().teams):
                is_selected = (i == TeamManager().RedTeam2.dropdownTeamNumber)
                if imgui.selectable(item, is_selected)[0] is True:
                    TeamManager().RedTeam2.dropdownTeamNumber = i
                if is_selected:
                    imgui.set_item_default_focus()
        imgui.end_combo()
    imgui.pop_item_width()
    # imgui.internal.pop_item_flag()
    imgui.same_line()

    if "Auto" in TeamManager().RedTeam2.status_message:
        imgui.push_style_color(imgui.COLOR_TEXT, 0.0, 1.0, 0.0, 1.0)
    else:
        imgui.push_style_color(imgui.COLOR_TEXT, 1.0, 0.75, 0.0, 1.0)

    imgui.text_unformatted(TeamManager().RedTeam2.status_message)
    imgui.pop_style_color()

    imgui.dummy(0.0, 50.0)
    imgui.same_line()
    overriden = False
    _, TeamManager().RedTeam2.overriden = imgui.checkbox("Manual channel override##R2", TeamManager().RedTeam2.overriden)

    if TeamManager().RedTeam2.overriden:
        imgui.same_line()
        imgui.push_item_width(100)
        imgui.input_text("##R2Textbox", TeamManager().RedTeam2.override_text, 50)
        imgui.pop_item_width()

def team3UI():
    imgui.text("Select Blue Alliance Team 1")
    imgui.push_item_width(150)
    # imgui.internal.push_item_flag(imgui.SELECTABLE_DISABLED, True)

    if imgui.begin_combo("##Dropdown3", TeamManager().teams[TeamManager().BlueTeam1.dropdownTeamNumber]):
        for i, item in enumerate(TeamManager().teams):
                is_selected = (i == TeamManager().BlueTeam1.dropdownTeamNumber)
                if imgui.selectable(item, is_selected)[0]:
                    TeamManager().BlueTeam1.dropdownTeamNumber = i
                if is_selected:
                    imgui.set_item_default_focus()
        imgui.end_combo()
    imgui.pop_item_width()
    # imgui.internal.pop_item_flag()
    imgui.same_line()

    if "Auto" in TeamManager().BlueTeam1.status_message:
        imgui.push_style_color(imgui.COLOR_TEXT, 0.0, 1.0, 0.0, 1.0)
    else:
        imgui.push_style_color(imgui.COLOR_TEXT, 1.0, 0.75, 0.0, 1.0)

    imgui.text_unformatted(TeamManager().BlueTeam1.status_message)
    imgui.pop_style_color()

    imgui.dummy(0.0, 50.0)
    imgui.same_line()
    _, TeamManager().BlueTeam1.overriden = imgui.checkbox("Manual channel override##B1", TeamManager().BlueTeam1.overriden)

    if TeamManager().BlueTeam1.overriden:
        imgui.same_line()
        imgui.push_item_width(100)
        _,TeamManager().BlueTeam1.override_text = imgui.input_text("##B1Textbox", TeamManager().BlueTeam1.override_text, 50)
        imgui.pop_item_width()

def team4UI():
    imgui.text("Select Blue Alliance Team 2")
    imgui.push_item_width(150)
    # imgui.internal.push_item_flag(imgui.SELECTABLE_DISABLED, True)

    if imgui.begin_combo("##Dropdown4", TeamManager().teams[TeamManager().BlueTeam2.dropdownTeamNumber]):
        for i, item in enumerate(TeamManager().teams):
                is_selected = (i == TeamManager().BlueTeam2.dropdownTeamNumber)
                if imgui.selectable(item, is_selected)[0]:
                    TeamManager().BlueTeam2.dropdownTeamNumber = i
                if is_selected:
                    imgui.set_item_default_focus()
        imgui.end_combo()
    imgui.pop_item_width()
    # imgui.internal.pop_item_flag()
    imgui.same_line()

    if "Auto" in TeamManager().BlueTeam2.status_message:
        imgui.push_style_color(imgui.COLOR_TEXT, 0.0, 1.0, 0.0, 1.0)
    else:
        imgui.push_style_color(imgui.COLOR_TEXT, 1.0, 0.75, 0.0, 1.0)

    imgui.text_unformatted(TeamManager().BlueTeam2.status_message)
    imgui.pop_style_color()

    imgui.dummy(0.0, 50.0)
    imgui.same_line()
    _, TeamManager().BlueTeam2.overriden = imgui.checkbox("Manual channel override##B2", TeamManager().BlueTeam2.overriden)

    if TeamManager().BlueTeam2.overriden:
        imgui.same_line()
        imgui.push_item_width(100)
        _,TeamManager().BlueTeam2.override_text = imgui.input_text("##B2Textbox", TeamManager().BlueTeam2.override_text, 50)
        imgui.pop_item_width()

def airodumpUI():
    s = ""
    if AirodumpManager().state == AIRODUMP_STATE.RUNNING:
        s = "airodump-ng - Scanning"
    else:
        s = "airodump-ng - Stopped"
    imgui.text(s)

    if imgui.begin_child("Console"):
        if imgui.begin_child("ScrollRegion##", 0, 160, border=True, flags=0):
            imgui.text(AirodumpManager().output)
        imgui.end_child()
    imgui.end_child()

def main():
    pygame.init()
    size = 1700, 950

    pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.OPENGL)
    pygame.display.set_caption('FTC Wifi Tools')

    imgui.create_context()
    impl = PygameRenderer()

    io = imgui.get_io()
    io.display_size = size

    io = imgui.get_io()
    new_font = io.fonts.add_font_from_file_ttf(
        "./assets/CodeNewRoman.otf", 16,
    )
    impl.refresh_font_texture()

    # Begin airodump by default
    AirodumpManager().start(INTERFACE_NAMES[0])

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Cleanup here
                AirodumpManager().stop()
                TSharkManager().stop()
                sys.exit(0)
            impl.process_event(event)
        impl.process_inputs()

        # Update the teams based on GUI
        TeamManager().update_teams(INTERFACE_NAMES)

        imgui.new_frame()

        imgui.set_next_window_size(1700, 950)
        imgui.set_next_window_position(0, 0)
        imgui.push_font(new_font)
        imgui.begin("Deauth Monitoring", flags=imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_RESIZE)

        imgui.separator()
        imgui.columns(2, "MainColumns", border=False)

        imgui.begin_child("LeftColumn")
        imgui.set_cursor_pos_x(imgui.get_window_width() - 150)

        if AirodumpManager().state == AIRODUMP_STATE.RUNNING:
            if imgui.button("Start Capturing", 150, 80):
                AirodumpManager().stop()
                TSharkManager().start()
        else:
            if imgui.button("Stop Capturing", 150, 80):
                AirodumpManager().start(INTERFACE_NAMES[0])
                TSharkManager().stop()
        imgui.dummy(0.0, 70.0)

        team1UI()
        imgui.dummy(0.0, 20.0)

        team2UI()
        imgui.dummy(0.0, 20.0)

        team3UI()
        imgui.dummy(0.0, 20.0)

        team4UI()

        airodumpUI()
        
        imgui.end_child()

        imgui.next_column()

        # TEXT AREA 1
        if "Not ready" in TeamManager().RedTeam1.capture_message:
            imgui.push_style_color(imgui.COLOR_TEXT, 1.0, 0.0, 0.0, 1.0)
        else:
            imgui.push_style_color(imgui.COLOR_TEXT, 1.0, 0.75, 0.0, 1.0)
        imgui.text_unformatted(TeamManager().RedTeam1.capture_message)
        imgui.pop_style_color()

        imgui.same_line()
        if imgui.begin_combo("##DropdownI1", INTERFACE_NAMES[TeamManager().RedTeam1.dropDownSelectedInterface], flags=imgui.COMBO_HEIGHT_LARGE):
            for i, item in enumerate(INTERFACE_NAMES):
                    is_selected = (i == TeamManager().RedTeam1.dropDownSelectedInterface)
                    if imgui.selectable(item, is_selected)[0]:
                        TeamManager().RedTeam1.dropDownSelectedInterface = i
                    if is_selected:
                        imgui.set_item_default_focus()
            imgui.end_combo()
        
        imgui.begin_child("TextArea1", 0, 190, border=True)
        imgui.text_unformatted(TeamManager().RedTeam1.tshark_output)
        if imgui.get_scroll_y() >= imgui.get_scroll_max_y():
            imgui.set_scroll_here_y(1.0)
        imgui.end_child()



        # TEXT AREA 2
        if "Not ready" in TeamManager().RedTeam2.capture_message:
            imgui.push_style_color(imgui.COLOR_TEXT, 1.0, 0.0, 0.0, 1.0)
        else:
            imgui.push_style_color(imgui.COLOR_TEXT, 1.0, 0.75, 0.0, 1.0)
        imgui.text_unformatted(TeamManager().RedTeam2.capture_message)
        imgui.pop_style_color()

        imgui.same_line()
        if imgui.begin_combo("##DropdownI2", INTERFACE_NAMES[TeamManager().RedTeam2.dropDownSelectedInterface], flags=imgui.COMBO_HEIGHT_LARGE):
            for i, item in enumerate(INTERFACE_NAMES):
                    is_selected = (i == TeamManager().RedTeam2.dropDownSelectedInterface)
                    if imgui.selectable(item, is_selected)[0]:
                        TeamManager().RedTeam2.dropDownSelectedInterface = i
                    if is_selected:
                        imgui.set_item_default_focus()
            imgui.end_combo()
        
        imgui.begin_child("TextArea2", 0, 190, border=True)
        imgui.text_unformatted(TeamManager().RedTeam2.tshark_output)
        if imgui.get_scroll_y() >= imgui.get_scroll_max_y():
            imgui.set_scroll_here_y(1.0)
        imgui.end_child()



        # TEXT AREA 3
        if "Not ready" in TeamManager().BlueTeam1.capture_message:
            imgui.push_style_color(imgui.COLOR_TEXT, 1.0, 0.0, 0.0, 1.0)
        else:
            imgui.push_style_color(imgui.COLOR_TEXT, 1.0, 0.75, 0.0, 1.0)
        imgui.text_unformatted(TeamManager().BlueTeam1.capture_message)
        imgui.pop_style_color()

        imgui.same_line()
        if imgui.begin_combo("##DropdownI3", INTERFACE_NAMES[TeamManager().BlueTeam1.dropDownSelectedInterface], flags=imgui.COMBO_HEIGHT_LARGE):
            for i, item in enumerate(INTERFACE_NAMES):
                    is_selected = (i == TeamManager().BlueTeam1.dropDownSelectedInterface)
                    if imgui.selectable(item, is_selected)[0]:
                        TeamManager().BlueTeam1.dropDownSelectedInterface = i
                    if is_selected:
                        imgui.set_item_default_focus()
            imgui.end_combo()
        
        imgui.begin_child("TextArea3", 0, 190, border=True)
        imgui.text_unformatted(TeamManager().BlueTeam1.tshark_output)
        if imgui.get_scroll_y() >= imgui.get_scroll_max_y():
            imgui.set_scroll_here_y(1.0)
        imgui.end_child()



        # TEXT AREA 4
        if "Not ready" in TeamManager().BlueTeam2.capture_message:
            imgui.push_style_color(imgui.COLOR_TEXT, 1.0, 0.0, 0.0, 1.0)
        else:
            imgui.push_style_color(imgui.COLOR_TEXT, 1.0, 0.75, 0.0, 1.0)
        imgui.text_unformatted(TeamManager().BlueTeam2.capture_message)
        imgui.pop_style_color()

        imgui.same_line()
        if imgui.begin_combo("##DropdownI4", INTERFACE_NAMES[TeamManager().BlueTeam2.dropDownSelectedInterface], flags=imgui.COMBO_HEIGHT_LARGE):
            for i, item in enumerate(INTERFACE_NAMES):
                    is_selected = (i == TeamManager().BlueTeam2.dropDownSelectedInterface)
                    if imgui.selectable(item, is_selected)[0]:
                        TeamManager().BlueTeam2.dropDownSelectedInterface = i
                    if is_selected:
                        imgui.set_item_default_focus()
            imgui.end_combo()
        
        imgui.begin_child("TextArea4", 0, 190, border=True)
        imgui.text_unformatted(TeamManager().BlueTeam2.tshark_output)
        if imgui.get_scroll_y() >= imgui.get_scroll_max_y():
            imgui.set_scroll_here_y(1.0)
        imgui.end_child()

        imgui.end()
        imgui.pop_font()

        gl.glClearColor(0, 0, 0, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        imgui.render()
        impl.render(imgui.get_draw_data())

        pygame.display.flip()


if __name__ == "__main__":
    load_interfaces()
    main()
