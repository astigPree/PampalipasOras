
from kivy.core.window import Window
Window.size = (1000 , 600)

from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.fitimage import FitImage
from kivy.uix.button import ButtonBehavior
from kivy.uix.modalview import ModalView
from kivy.uix.textinput import TextInput
from kivymd.uix.gridlayout import MDGridLayout

from kivy.lang.builder import Builder
from kivy.core.text import LabelBase
from kivy.properties import StringProperty , NumericProperty , ObjectProperty , DictProperty , ListProperty
from kivy.clock import Clock

import backend
import copy

# ======= Image Full Viewer
class FullViewerImage( ButtonBehavior ,FitImage ) :
    view : ModalView = None

    def on_press(self , *args):
        if self.view :
            return
        self.view = ModalView( size_hint = ( 0.9 , 0.9 ))
        widget = BoxLayout()
        widget.add_widget(
            FitImage(
                source=self.source,
                radius=(5, 5, 5, 5)
            )
        )
        self.view.add_widget(widget)

    def on_release(self):
        self.view.open()


# ======= Cottage Selected Modifier
class CottageInformationInput(TextInput):

    def checkText(self):
        new_text = ''
        for letter in self.text :
            if letter.isdigit() :
                new_text += letter
            if '.' == letter and letter not in new_text :
                new_text += letter

        self.text = new_text

class CottageInModifier(BoxLayout):
    image = StringProperty('Cottage Pictures/coca cola,30.png')
    name = StringProperty('')
    price = NumericProperty(200)
    persons = NumericProperty(1)
    items = NumericProperty(0)
    electric = NumericProperty(0)
    water = NumericProperty(0)
    total = NumericProperty(200)
    cottage_id = NumericProperty(0)

    def update(self , image : str , name : str ,price : float , cottage_id : int ):
        self.image = image
        self.name = name
        self.price = price
        self.total = price
        self.cottage_id = cottage_id

    def checkInput(self, info : str , value : str ):
        if not value :
            value = 0
        if info == 'persons' :
            if int(value) < 1 :
                self.persons = 1
            else :
                self.persons = float(value)
        if info == 'items' :
            self.items = float(value)
        if info == 'electric' :
            self.electric = float(value)
        if info == 'water' :
            self.water = float(value)

        self.total = round( (self.persons * self.price) + self.items + self.electric + self.water , 2)

class CottageSelectedContainer(BoxLayout) :
    cottage_selected_container : MDGridLayout = ObjectProperty(None)

    def remove_cottage(self , cottage_id : int ):
        for cottage in self.cottage_selected_container.children :
            if cottage.cottage_id == cottage_id :
                self.cottage_selected_container.remove_widget(cottage)

    def add_cottage(self , cottage : CottageInModifier ):
        self.cottage_selected_container.add_widget(cottage)

class CottageSelectedModifier(BoxLayout) :

    cottage_ids : list[str , ... ] = ListProperty([])
    cottage_selected_container : CottageSelectedContainer = ObjectProperty(None)

    def on_kv_post(self, base_widget):
        Clock.schedule_interval(self.checkIfThereIsSelectedCottage , 1 / 30 )
        Clock.schedule_interval(self.checkIfThereIsUnselectedCottage , 1 / 30 )

    def checkIfThereIsSelectedCottage(self , interval ):
        widgets : list[CottageInModifier , ...] = []
        for cottage in self.parent.datas.get_all_data() :
            if cottage['selected'] and cottage['id'] not in self.cottage_ids :
                widget = CottageInModifier()
                widget.update(cottage['filename'] , cottage['name'] , cottage['price'] , cottage['id'])
                widgets.append(widget)
                self.cottage_ids.append(cottage['id'])

        for widget in widgets :
            self.cottage_selected_container.add_cottage(widget)

    def checkIfThereIsUnselectedCottage(self , interval ):
        for cottage in self.parent.datas.get_all_data() :
            if cottage['id'] in self.cottage_ids and not cottage['selected'] :
                self.cottage_ids.remove(cottage['id'])
                self.cottage_selected_container.remove_cottage(cottage['id'])


    # ----> Parent Connections

# ======= Cottage Selections
class CottageInSelections(BoxLayout) :

    image = StringProperty('')
    price = NumericProperty(200)
    name = StringProperty('')
    datas : backend.CottageDataManagement.data = DictProperty({'selected' : False})

    def update(self , image : str , name : str , price : int  , datas : dict ):
        self.image = image
        self.name = name
        self.price = price
        self.datas = datas

    def selectIt(self):
        self.datas['selected'] = not self.datas['selected']
        self.parent.parent.parent.parent.selectingCottage(self.datas['id'] , self.datas['selected'] )


class CottageSelectionsContainer(BoxLayout):
    list_of_cottage: MDGridLayout = ObjectProperty(None)


class CottageSelections(BoxLayout):

    cottage_container: CottageSelectionsContainer = ObjectProperty(None)

    # ----> Logic Variables
    current = StringProperty('all')

    def addWidgetInList(self , widget : CottageInSelections):
        self.cottage_container.list_of_cottage.add_widget(widget)

    def displayAll(self):
        if self.current == 'all' :
            return
        self.cottage_container.list_of_cottage.clear_widgets()
        widgets = []
        for data in self.parent.datas.get_all_data():
            widget = CottageInSelections()
            widget.update(data['filename'], data['name'], data['price'], data)
            widgets.append(widget)
        for widget in widgets:
            self.addWidgetInList(widget)

    def displaySelected(self):
        if self.current == 'selected' :
            return
        self.cottage_container.list_of_cottage.clear_widgets()
        widgets = []
        for data in self.parent.datas.get_all_data():
            if data['selected'] :
                widget = CottageInSelections()
                widget.update(data['filename'], data['name'], data['price'], data)
                widgets.append(widget)
        for widget in widgets:
            self.addWidgetInList(widget)

    def displayUnselected(self):
        if self.current == 'unselected' :
            return
        self.cottage_container.list_of_cottage.clear_widgets()
        widgets = []
        for data in self.parent.datas.get_all_data():
            if not data['selected']:
                widget = CottageInSelections()
                widget.update(data['filename'], data['name'], data['price'], data)
                widgets.append(widget)
        for widget in widgets:
            self.addWidgetInList(widget)

    # ----> Parent Connections
    def selectingCottage(self, cottage_id: int, value: bool):
        self.parent.updateCottageData(cottage_id , value)



# ======= Main Widget
class MainWidget(BoxLayout) :

    datas = backend.CottageDataManagement()
    cottage_selections: CottageSelections = ObjectProperty(None)
    cottage_modifier: CottageSelectedModifier = ObjectProperty(None)



    def on_kv_post(self, base_widget):
        widgets = []
        for data in self.datas.get_all_data():
            widget = CottageInSelections()
            widget.update( data['filename'] , data['name'] , data['price'] , data )
            widgets.append(widget)
            print(data)
        for widget in widgets :
            self.cottage_selections.addWidgetInList(widget)
            print(widget)

    # ------> Child Activities
    def updateCottageData(self, cottage_id : int , val : bool ):
        if val :
            self.datas.select_item(cottage_id)
        else :
            self.datas.unselect_item(cottage_id)



# ======== Application
class CottageApp(MDApp):

    def build(self):
        return Builder.load_file('design.kv')

if __name__ == '__main__':
    LabelBase.register( name='font' , fn_regular="fonts/summary.ttf")
    LabelBase.register(name='numfont', fn_regular="fonts/numfont.ttf")
    CottageApp().run()