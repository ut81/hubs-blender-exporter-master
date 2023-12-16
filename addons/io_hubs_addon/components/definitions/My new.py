import bpy
from bpy.types import Operator

from ..models import link
from ..gizmos import CustomModelGizmo, bone_matrix_world
from bpy.props import FloatProperty, StringProperty
from ..hubs_component import HubsComponent
from ..types import Category, PanelType, NodeType
from .networked import migrate_networked

class MyTestButtonOperator(Operator):
    bl_idname = "link.my_test_button"
    bl_label = "My Test Button"
    bl_options = {'REGISTER', 'UNDO'}
    href: StringProperty(name="Link URL", description="Link URL",
                         default="https://test.org")
    polyCountWarning: FloatProperty(
        name="Polycount Warning", description="test warning", default=20.0)
    TextureSize: FloatProperty(
        name="Texture Size Warning", description="test warning", default=20.0)
    FileSize: FloatProperty(
        name="FileSize Warning", description="test warning", default=20.0)

    def execute(self, context):
        # Access all properties from the property group
        href = self.href
        poly_count_warning = self.polyCountWarning
        texture_size = self.TextureSize
        file_size = self.FileSize

        self.report({'INFO'}, f"Button Clicked! Href: {href}, Polycount Warning: {poly_count_warning}, Texture Size: {texture_size}, File Size: {file_size}")
        return {'FINISHED'}
class Link(HubsComponent):
    _definition = {
        'name': 'my-new',
        'display_name': 'My New',
        'category': Category.ELEMENTS,
        'node_type': NodeType.NODE,
        'panel_type': [PanelType.OBJECT, PanelType.BONE],
        'icon': 'LINKED',
        'deps': ['networked'],

        'version': (1, 0, 0)
    }
    href: StringProperty(name="Link URL", description="Link URL",
                         default="https://test.org")
    polyCountWarning: FloatProperty(
        name="Polycount Warning", description="test warning", default=20.0)
    TextureSize: FloatProperty(
        name="Texture Size Warning", description="test warning", default=20.0)
    FileSize: FloatProperty(
        name="FileSize Warning", description="test warning", default=20.0)

    
    def draw(self, context, layout, panel):
        row = layout.column()
        row.prop(data=self, property="href")
        row.prop(data=self, property="polyCountWarning")
        row.prop(data=self, property="TextureSize")
        row.prop(data=self, property="FileSize")
        
        row = layout.row()
        op = row.operator("link.my_test_button", text="Click Me!")
        op.href = self.href
        op.polyCountWarning = self.polyCountWarning
        op.TextureSize = self.TextureSize
        op.FileSize = self.FileSize

        
    @classmethod
    def register(cls):
        bpy.utils.register_class(MyTestButtonOperator)

    @classmethod
    def unregister(cls):
        bpy.utils.unregister_class(MyTestButtonOperator)
    
        

    def migrate(self, migration_type, panel_type, instance_version, host, migration_report, ob=None):
        migration_occurred = False
        if instance_version < (1, 0, 0):
            migration_occurred = True
            migrate_networked(host)

        return migration_occurred

    @classmethod
    def update_gizmo(cls, ob, bone, target, gizmo):
        if bone:
            mat = bone_matrix_world(ob, bone)
        else:
            mat = ob.matrix_world.copy()

        gizmo.hide = not ob.visible_get()
        gizmo.matrix_basis = mat

    @classmethod
    def create_gizmo(cls, ob, gizmo_group):
        gizmo = gizmo_group.gizmos.new(CustomModelGizmo.bl_idname)
        gizmo.object = ob
        setattr(gizmo, "hubs_gizmo_shape", link.SHAPE)
        gizmo.setup()
        gizmo.use_draw_scale = False
        gizmo.use_draw_modal = False
        gizmo.color = (0.8, 0.8, 0.8)
        gizmo.alpha = 0.5
        gizmo.scale_basis = 1.0
        gizmo.hide_select = True
        gizmo.color_highlight = (0.8, 0.8, 0.8)
        gizmo.alpha_highlight = 1.0

        return gizmo
