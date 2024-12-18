import bpy

from .const import INTERNAL_NAME, ADDON_NAME, VERSION_STR
from . import utils as u

class PT_SimpleToolbox(bpy.types.Panel):
    bl_idname = 'OBJECT_PT_quick_toolbox'
    bl_label = f'{ADDON_NAME} ({VERSION_STR})'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'
    # bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        addon_props = u.get_addon_props()
        addon_prefs = bpy.context.preferences.addons[INTERNAL_NAME].preferences
        
        layout = self.layout

        row = layout.row()
        row.prop(addon_prefs, "experimental_features", text="Experimental Features", icon="EXPERIMENTAL")

        # Dev Tools
        dev_tools_box = layout.box()
        dev_tools_box.prop(addon_props, "show_dev_tools", icon="TRIA_DOWN" if addon_props.show_dev_tools else "TRIA_RIGHT", emboss=False)
        if addon_props.show_dev_tools:
            row = dev_tools_box.row()
            row.operator("script.reload", text="Reload All Scripts", icon="PACKAGE")
            reload_user_defined_box = dev_tools_box.box()
            row = reload_user_defined_box.row()
            row.prop(addon_props, "reload_modules_prop")
            row = reload_user_defined_box.row()
            row.operator("r0tools.reload_named_scripts", icon="TOOL_SETTINGS")
            if addon_prefs.experimental_features:
                row = dev_tools_box.row()
                row.operator("image.reload", icon="IMAGE_DATA")
        
        # Object Ops
        object_ops_box = layout.box()
        object_ops_box.prop(addon_props, "show_object_ops", icon="TRIA_DOWN" if addon_props.show_object_ops else "TRIA_RIGHT", emboss=False)
        if addon_props.show_object_ops:

            row = object_ops_box.row(align=True)
            row.operator("r0tools.clear_custom_split_normals_data")

            row = object_ops_box.row(align=True)
            row.operator("r0tools.clear_all_objects_children")
            
            # Object Sets Editor
            if addon_prefs.experimental_features:
                object_sets_box = object_ops_box.box()
                row = object_sets_box.row()
                row.prop(addon_props, "show_object_sets", icon="TRIA_DOWN" if addon_props.show_object_sets else "TRIA_RIGHT", emboss=False)
                if addon_props.show_object_sets:
                    row = object_sets_box.row()
                    split = row.split(factor=0.9)

                    # Left Section
                    col = split.column()
                    col.template_list(
                        "R0PROP_UL_ObjectSetsList",
                        "object_sets",
                        u.get_addon_props(),  # Collection owner
                        "object_sets",                     # Collection property
                        u.get_addon_props(),  # Active item owner
                        "object_sets_index",               # Active item property
                        rows=6
                    )

                    # Right side
                    col = split.column(align=True)
                    col.operator("r0tools.add_object_set_popup")
                    col.operator("r0tools.remove_object_set")

                    # Bottom
                    row = object_sets_box.row(align=True)
                    split = row.split(factor=0.65)
                    row_col = split.row(align=True)
                    row_col.operator("r0tools.add_to_object_set")
                    row_col.operator("r0tools.remove_from_object_set")
                    #
                    row_col = split.row()
                    row_col.operator("r0tools.select_object_set")

                # Custom Properties UI List
                custom_properties_box = object_ops_box.box()
                row = custom_properties_box.row()
                row.prop(addon_props, "show_custom_property_list_prop", icon="TRIA_DOWN" if addon_props.show_custom_property_list_prop else "TRIA_RIGHT", emboss=False)
                if addon_props.show_custom_property_list_prop:
                    row = custom_properties_box.row()
                    row.template_list(
                        "R0PROP_UL_CustomPropertiesList",
                        "custom_property_list",
                        u.get_addon_props(),  # Collection owner
                        "custom_property_list",            # Collection property
                        u.get_addon_props(),  # Active item owner
                        "custom_property_list_index",      # Active item property
                        rows=6
                    )
                
                # Clear Custom Properties
                row = custom_properties_box.row()
                row.operator("r0tools.clear_custom_properties")
        
        # Mesh Ops
        mesh_ops_box = layout.box()
        mesh_ops_box.prop(addon_props, "show_mesh_ops", icon="TRIA_DOWN" if addon_props.show_mesh_ops else "TRIA_RIGHT", emboss=False)
        if addon_props.show_mesh_ops:
            # Nth Edges Operator
            row = mesh_ops_box.row(align=True)
            row.operator("r0tools.nth_edges")
            row = mesh_ops_box.row(align=True)
            row.operator("r0tools.rotation_from_selection")
            
            # Clear Sharp Edges on Axis
            clear_sharp_edges_box = mesh_ops_box.box()
            row = clear_sharp_edges_box.row(align=True)
            clear_sharp_edges_box.prop(addon_props, "show_clear_sharps_on_axis", icon="TRIA_DOWN" if addon_props.show_clear_sharps_on_axis else "TRIA_RIGHT", emboss=False)
            if addon_props.show_clear_sharps_on_axis:
                row = clear_sharp_edges_box.row(align=True)
                row.prop(addon_prefs, "clear_sharp_axis_float_prop", text="Threshold")
                row = clear_sharp_edges_box.row(align=True)
                row.scale_x = 5
                row.operator("r0tools.clear_sharp_axis_x", text="X")
                row.operator("r0tools.clear_sharp_axis_y", text="Y")
                row.operator("r0tools.clear_sharp_axis_z", text="Z")
        
        # Externals
        externals_box = layout.box()
        externals_box.prop(addon_props, "show_ext_ops", icon="TRIA_DOWN" if addon_props.show_ext_ops else "TRIA_RIGHT", emboss=False)
        if addon_props.show_ext_ops:
            row = externals_box.row(align=True)
            row.label(text="ZenUV Texel Density")
            row = externals_box.row(align=True)
            row.prop(addon_prefs, "zenuv_td_prop", text="TD:")
            row.prop(addon_prefs, "zenuv_td_unit_prop", text="Unit")
            row = externals_box.row(align=True)
            row.operator("r0tools.ext_zenuv_set_td")

        # Heavy Experimentals
        if addon_prefs.experimental_features:
            row = layout.row()
            row.label(text="EXPERIMENTAL", icon="EXPERIMENTAL")
            lods_box = layout.box()
            row = lods_box.row()
            row.label(text="LODs")
            row = lods_box.row()
            row.operator("r0tools.experimental_op_1")
            row = lods_box.row()
            row.prop(addon_props, "screen_size_pct_prop", text="Screen Size (%):")


# -------------------------------------------------------------------
#   Register & Unregister
# -------------------------------------------------------------------

classes = [
    PT_SimpleToolbox
]

depsgraph_handlers = [
    u.continuous_property_list_update
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    for handler in depsgraph_handlers:
        if handler not in bpy.app.handlers.depsgraph_update_post:
            print(f"[DEBUG] Registering Handler {handler}")
            bpy.app.handlers.depsgraph_update_post.append(handler)

def unregister():
    for handler in depsgraph_handlers:
        try:
            if handler in bpy.app.handlers.depsgraph_update_post:
                bpy.app.handlers.depsgraph_update_post.remove(handler)
        except Exception as e:
            print(f"Error removing handler {handler}: {e}")

    for cls in classes:
        bpy.utils.unregister_class(cls)
