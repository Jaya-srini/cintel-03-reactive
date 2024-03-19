import plotly.express as px
from shiny.express import input, ui
from shiny import render, reactive, req
from shinywidgets import render_plotly
import palmerpenguins  # This package provides the Palmer Penguins dataset
import pandas as pd
import seaborn as sns

#Load palmer penguins dataset
penguins_df = palmerpenguins.load_penguins()

#name my page
ui.page_opts(title='Jaya Penguin Data', fillable=True)

# Add a Shiny UI sidebar for user interaction
# Use the ui.sidebar() function to create a sidebar
# Set the open parameter to "open" to make the sidebar open by default
# Use a with block to add content to the sidebar

with ui.sidebar(open='open'): #Set to open to open sidebar by default
#Second level header to the sidebar
    ui.h2("Sidebar")
#Use ui.input_selectize() to create a dropdown input to choose a column
#   pass in three arguments:
#   the name of the input (in quotes), e.g., "selected_attribute"
#   the label for the input (in quotes)
#   a list of options for the input (in square brackets) 
#   e.g. ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
    ui.input_selectize(
        "selected_attribute", 
        "Select Attribute",
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
    )
# Use ui.input_numeric() to create a numeric input for the number of Plotly histogram bins
#   pass in two arguments:
#   the name of the input (in quotes), e.g. "plotly_bin_count"
#   the label for the input (in quotes)

    ui.input_numeric("plotly_bin_count", "ploty bin number", 30)


# Use ui.input_slider() to create a slider input for the number of Seaborn bins
#   pass in four arguments:
#   the name of the input (in quotes), e.g. "seaborn_bin_count"
#   the label for the input (in quotes)
#   the minimum value for the input (as an integer)
#   the maximum value for the input (as an integer)
#   the default value for the input (as an integer)
    ui.input_slider("seaborn_bin_count", "seaborn bin number", 1, 60, 10)

# Use ui.input_checkbox_group() to create a checkbox group input to filter the species
#   pass in five arguments:
#   the name of the input (in quotes), e.g.  "selected_species_list"
#   the label for the input (in quotes)
#   a list of options for the input (in square brackets) as ["Adelie", "Gentoo", "Chinstrap"]
#   a keyword argument selected= a list of selected options for the input (in square brackets)
#   a keyword argument inline= a Boolean value (True or False) as you like
    ui.input_checkbox_group(
        "selected_species_list",
        "select species",
        ["Adelie", "Gentoo", "Chinstrap"],selected=["Gentoo", "Chinstrap"],inline=True,
    )
#Use ui.hr()
    ui.hr()

# Use ui.a() to add a hyperlink to the sidebar
#   pass in two arguments:
#   the text for the hyperlink (in quotes), e.g. "GitHub"
#   a keyword argument href= the URL for the hyperlink (in quotes), e.g. your GitHub repo URL
#   a keyword argument target= "_blank" to open the link in a new tab

ui.a("My GitHub", href="https://github.com/Jaya-srini/cintel-02-data-/blob/main/app.py", target="_blank")

# Display data table

with ui.accordion(id="acc", open="closed"):
    with ui.accordion_panel("Data Table"):
        @render.data_frame
        def penguin_datatable():
            return render.DataTable(penguins_df)

# Display data grid
    with ui.accordion_panel("Data Grid"):
        @render.data_frame
        def penguin_datagrid():
            return render.DataGrid(penguins_df)

# Creates a Plotly Histogram showing all species

with ui.card(full_screen=True):
    ui.card_header("Plotly Histogram")
    
    @render_plotly
    def plotly_histogram():
        return px.histogram(
            penguins_df, x=input.selected_attribute(), nbins=input.plotly_bin_count()
        )

# Creates a Seaborn Histogram showing all species

with ui.card(full_screen=True):
    ui.card_header("Seaborn Histogram")

    @render.plot(alt="Seaborn Histogram")
    def seaborn_histogram():
        histplot = sns.histplot(data=penguins_df, x="body_mass_g", bins=input.seaborn_bin_count())
        histplot.set_title("Palmer Penguins")
        histplot.set_xlabel("Mass")
        histplot.set_ylabel("Count")
        return histplot
        
# Creates a Plotly Scatterplot showing all species

with ui.card(full_screen=True):
    ui.card_header("Plotly Scatterplot: Species")

    @render_plotly
    def plotly_scatterplot():
        return px.scatter(penguins_df,
            x="bill_length_mm",
            y="body_mass_g",
            color="species",
            title="Penguins Plot",
            labels={
                "bill_length_mm": "Bill Length (mm)",
                "body_mass_g": "Body Mass (g)",
            },
            size_max=8, 
                         )

ui.page_opts(title='Jaya Penguin Data', fillable=True)
