# coding=UTF-8
# ex:ts=4:sw=4:et=on

# Author: Mathijs Dumon
# This work is licensed under the Creative Commons Attribution-ShareAlike 3.0 Unported License. 
# To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0/ or send
# a letter to Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.

import gtk
from gtkmvc import Controller

import settings

from generic.utils import get_case_insensitive_glob
from generic.views import InlineObjectListStoreView
from generic.controllers import BaseController, ChildObjectListStoreController

from phases.controllers import EditLayerController, EditAtomRelationsController, EditUnitCellPropertyController
from phases.views import EditComponentView, EditUnitCellPropertyView
from phases.models import Component

class EditComponentController(BaseController):
    """ 
        Controller for the component edit view
    """
    layer_view = None
    layer_controller = None
    
    interlayer_view = None
    interlayer_controller = None
    
    atom_relations_view = None
    atom_relations_controller = None
    
    ucpa_view = None
    ucpa_controller = None
    
    ucpb_view = None
    ucpb_controller = None

    widget_handlers = { 
        'custom': 'custom_handler',
        'combo':  'combo_handler' 
    }

    def __init__(self, *args, **kwargs):
        BaseController.__init__(self, *args, **kwargs)
        
        self.layer_view = InlineObjectListStoreView(parent=self.view)
        self.layer_controller = EditLayerController("_layer_atoms", model=self.model, view=self.layer_view, parent=self)
        
        self.interlayer_view = InlineObjectListStoreView(parent=self.view)
        self.interlayer_controller = EditLayerController("_interlayer_atoms", model=self.model, view=self.interlayer_view, parent=self)
        
        self.atom_relations_view = InlineObjectListStoreView(parent=self.view)
        self.atom_relations_controller = EditAtomRelationsController("_atom_relations", model=self.model, view=self.atom_relations_view, parent=self)
        
        self.ucpa_view = EditUnitCellPropertyView(parent=self.view)
        self.ucpa_controller = EditUnitCellPropertyController(extra_props=[(self.model, "cell_b", "B cell length"),], model=self.model.ucp_a, view=self.ucpa_view, parent=self)
        
        self.ucpb_view = EditUnitCellPropertyView(parent=self.view)
        self.ucpb_controller = EditUnitCellPropertyController(extra_props=[(self.model, "cell_a", "A cell length"),], model=self.model.ucp_b, view=self.ucpb_view, parent=self)

    def reset_combo_box(self):
        if self.model is not None and self.model.parent is not None:
            combo = self.view["component_linked_with"]
            combo.clear()
            if self.model.parent.based_on is not None:
                tv_model = self.model.parent.based_on.components
                combo.set_model(tv_model)
                cell = gtk.CellRendererText() #FIXME!
                combo.pack_start(cell, True)
                combo.add_attribute(cell, 'text', tv_model.c_name)
                for row in tv_model:
                    if tv_model.get_user_data(row.iter) == self.model.linked_with:
                        combo.set_active_iter (row.iter)
                        break
            else:
                combo.set_model(None)

    @staticmethod
    def combo_handler(self, intel, prefix):
        if intel.name == "linked_with":
            self.reset_combo_box()
        else: return False
        return True
         
    @staticmethod
    def custom_handler(self, intel, prefix):
        if intel.name == "layer_atoms":
            self.view.set_layer_view(self.layer_view.get_top_widget())
        elif intel.name == "interlayer_atoms":
            self.view.set_interlayer_view(self.interlayer_view.get_top_widget())
        elif intel.name ==  "atom_relations":
            self.view.set_atom_relations_view(self.atom_relations_view.get_top_widget())
        elif intel.name in ("ucp_a", "ucp_b"):
            self.view.set_ucpa_view(self.ucpa_view.get_top_widget())
            self.view.set_ucpb_view(self.ucpb_view.get_top_widget())
        else: return False
        return True
         
    def register_adapters(self):
        BaseController.register_adapters(self)
        self.update_sensitivities()

    def update_sensitivities(self):
        can_inherit = (self.model.linked_with != None)

        def update(widget, name):
            self.view[widget].set_sensitive(not (can_inherit and getattr(self.model, "inherit_%s" % name)))
            self.view[widget].set_visible(not (can_inherit and getattr(self.model, "inherit_%s" % name)))
            self.view["component_inherit_%s" % name].set_sensitive(can_inherit)
        for name in ("d001", "default_c", "delta_c"):
            update("container_%s" % name, name.replace("data_", "", 1))
        for name in ("interlayer_atoms", "layer_atoms", "atom_relations", "ucp_a", "ucp_b"):
            update("container_%s" % name, name)


    # ------------------------------------------------------------
    #      Notifications of observable properties
    # ------------------------------------------------------------
    @Controller.observe("inherit_layer_atoms", assign=True)
    @Controller.observe("inherit_interlayer_atoms", assign=True)
    @Controller.observe("inherit_atom_relations", assign=True)
    @Controller.observe("inherit_ucp_a", assign=True)
    @Controller.observe("inherit_ucp_b", assign=True)
    @Controller.observe("inherit_d001", assign=True)
    @Controller.observe("inherit_default_c", assign=True)
    @Controller.observe("inherit_delta_c", assign=True)
    def notif_change_inherit(self, model, prop_name, info):
        self.update_sensitivities()
    
    @Controller.observe("name", assign=True)
    def notif_name_changed(self, model, prop_name, info):
        self.model.parent.components.on_item_changed(self.model)

    @Controller.observe("linked_with", assign=True)
    def notif_linked_with_changed(self, model, prop_name, info):
        self.reset_combo_box()


    # ------------------------------------------------------------
    #      GTK Signal handlers
    # ------------------------------------------------------------
    def on_linked_with_changed(self, combo, user_data=None):
        itr = combo.get_active_iter()
        if itr != None:
            val = combo.get_model().get_user_data(itr)
            self.model.linked_with = val
            self.update_sensitivities()
            return
        combo.set_active(-1)
        self.update_sensitivities()
        self.model.linked_with = None

class ComponentsController(ChildObjectListStoreController):
    """ 
        Controller for the components ObjectListStore
    """
    model_property_name = "components"
    columns = [ ("Component name", "c_name") ]
    delete_msg = "Deleting a component is irreverisble!\nAre You sure you want to continue?"
    file_filters = [("Component file", get_case_insensitive_glob("*.CMP")),]

    def get_new_edit_view(self, obj):
        if isinstance(obj, Component):
            return EditComponentView(parent=self.view)
        else:
            return ChildObjectListStoreController.get_new_edit_view(self, obj)
        
    def get_new_edit_controller(self, obj, view, parent=None):
        if isinstance(obj, Component):
            return EditComponentController(model=obj, view=view, parent=parent)
        else:
            return ChildObjectListStoreController.get_new_edit_controller(self, obj, view, parent=parent)

    def load_components(self, filename):
        old_comps = self.get_selected_objects()
        num_oc = len(old_comps)
        new_comps = list()
        for comp in Component.load_components(filename, parent=self.model):
            comp.resolve_json_references()
            new_comps.append(comp)
        num_nc = len(new_comps)
        if num_oc != num_nc:
            self.run_information_dialog("The number of components to import must equal the number of selected components!")
            return
        else:
            self.select_object(None)
            print "Importing components..."
            #replace component(s):
            for old_comp, new_comp in zip(old_comps, new_comps):
                self.liststore.replace_item(old_comp, new_comp)
                #this will break any links as well with other components:
                old_comp.parent = None
            #self.select_object(new_comp)

    # ------------------------------------------------------------
    #      GTK Signal handlers
    # ------------------------------------------------------------
    def on_save_object_clicked(self, event):
        def on_accept(dialog):
            print "Exporting components..."
            filename = self.extract_filename(dialog)
            Component.save_components(self.get_selected_objects(), filename=filename)
        self.run_save_dialog("Export components", on_accept, parent=self.view.get_toplevel())
        return True
        
    def on_load_object_clicked(self, event):
        def on_accept(dialog):
            self.load_components(dialog.get_filename())
        self.run_load_dialog("Import components", on_accept, parent=self.view.get_toplevel())
        return True
