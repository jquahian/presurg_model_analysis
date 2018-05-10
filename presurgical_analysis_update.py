import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


df = pd.read_csv('presurgical_requests_datasheet.csv', delimiter=',')

colors = ['#eafffb', '#c0e0db', '#a2dbd2', '#72c1b5', 
			'#50aa9d', '#34998a', '#187567']

groups = ['requestor', 'pathology', 'printer_type']

measures = ['material_quantity', 'material_cost', 'operator_cost', 'cost', 'segment_time', 'post_process_time', 'print_time']

measures_time = ['segment_time', 'print_time', 'post_process_time']

measures_cost = ['material_cost', 'operator_cost']

calcs = ['mean', 'sum']

axis_font_size = 14

def single_plotter():
	for group in groups:
		for measure in measures:
			for calc in calcs:

				if 'quantity' in measure:
					unit = '(g or mL)'
				elif 'cost' in measure:
					unit = '($CAD)'
				elif 'time' in measure:
					unit = '(mins)'

				if calc == 'mean':
					calc_word = 'Average'
					df_std = df.groupby(group)[measure].std()
					y_err = df_std.tolist()
					capsize = 10
					df_single_plot = df.groupby(group)[measure].mean()
				elif calc =='sum':
					calc_word = 'Total'
					y_err=0
					capsize=0
					df_single_plot = df.groupby(group)[measure].sum()
				
				ax = df_single_plot.plot(kind='bar',
											rot=75,
											yerr=y_err,
											capsize=capsize, 
											color=colors, 
											edgecolor='#000000', 
											figsize=(11.5,8), 
											title='{} vs. {} {}'.format(group.replace('_', ' ').title(), calc_word, measure.replace('_', ' ').title()))
				
				ax.set_xlabel(group.replace('_', ' ').title(), 
								fontsize=axis_font_size, 
								fontweight='bold')

				ax.set_ylabel('{} {} {}'.format(calc_word, measure.replace('_', ' ').title(), unit), 
								fontsize=axis_font_size, 
								fontweight='bold')

				ax.tick_params(labelsize=14)

				ax.title.set_size(20)

				plt.savefig('Plots/{}_wrt_{}_{}.png'.format(group, calc, measure), 
							format='png', 
							dpi=300, 
							bbox_inches='tight')

				plt.clf()


def multi_measure_plotter(measures, measure_type):
	for group in groups:
		for calc in calcs:

			if measure_type == 'time':
				title = 'Time per Fabrication Step'
				unit = '(mins)'
			elif measure_type == 'cost':
				title = 'Cost Breakdown'
				unit = '($CAD)'

			if calc == 'mean':
				calc_word = 'Average'
				df_multi_plot = df.groupby(group)[measures].mean()
			elif calc =='sum':
				calc_word = 'Total'
				df_multi_plot = df.groupby(group)[measures].sum()

			ax = df_multi_plot.plot.bar(rot=75,
										color=colors,
										edgecolor='#000000',
										figsize=(11,8.5),
										title='{} {} per {}'.format(calc_word, title, group.title().replace('_', ' ')))
		
			ax.set_xlabel('{}'.format(group.title().replace('_', ' ')), 
							fontsize=axis_font_size, 
							fontweight='bold')

			ax.set_ylabel('{} {} {}'.format(calc_word, title, unit), 
							fontsize=axis_font_size, 
							fontweight='bold')

			ax.tick_params(labelsize=10)

			ax.title.set_size(20)

			ax.legend(loc='best', fontsize=14, frameon=False)


			plt.savefig('Plots/Multi Plots/{}_{}_per_{}.png'.format(calc_word, title.lower().replace(' ', '_'), group), 
						bbox_inches='tight', 
						format='png', 
						dpi=300)

			plt.clf()


def summarized_data():
	with open('data_overview.txt', 'w') as text_file:

		num_unique_requestors = df['requestor'].value_counts()
		num_unique_reviewers = df['reviewing_radiologist'].value_counts()
		num_unique_pathologies = df['pathology'].value_counts()
		num_modalities = df['modality'].value_counts()
		num_pins = df['num_pins'].sum()
		num_magnets = df['num_magnets'].sum()

		print(f'Number of Unique Requestors: \n{num_unique_requestors} \n\nNumber of Unique Reviewers: \n{num_unique_reviewers} \n\nNumber of Unique Pathologies: \n{num_unique_pathologies} \n\nNumber of Imaging Modalities: \n{num_modalities} \n\nNumber of Pins used during Assembly: \n{num_pins} \n\nNumber of Mangets used during Assembly: \n{num_magnets}', file=text_file)

def summarized_cost_data(*arg):
	with open('summarized_cost_data.txt', 'w') as text_file:
		for args in arg:
			total = df[args].sum()
			avg = df[args].mean()
			std = df[args].std()

			print(args + f'\nTotal: ${round(total, 2)} \nAverage: ${round(avg, 2)} \nstdev: +/-{round(std, 2)}\n\n', file = text_file)

	summarized_data()

def desc_corr():
	df.corr().to_csv('corr.csv')
	df.describe().to_csv('describe.csv')


# use this to plot a single group vs. a single measure
single_plotter()

# use this to plot multiple groups vs. multiple measures
multi_measure_plotter(measures_time, 'time')
multi_measure_plotter(measures_cost, 'cost')

# use this to create a two text summaries of the data
summarized_cost_data('cost', 'material_cost', 'operator_cost', 'segment_time', 'post_process_time', 'print_time', 'material_quantity')

# use this to generate descriptive measures and correlation
desc_corr()

print('All caught-up!')