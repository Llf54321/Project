# %%
def plot_other_energy_partial_beb(energy, total_beb_70,df,num,partial_beb_70):
    import matplotlib.pylab as plt
    import numpy as np
    total_beb = df[df['energy']==int('{0}'.format(energy))]['total_beb'].values
    x = [int('{0}'.format(energy))]*num
    y = np.array(partial_beb_70)*total_beb/total_beb_70

    plt.scatter(x,y,marker='X', color='coral')

def plot_energy_vs_total_and_partial_beb(name, save=False):
    import sqlite3
    import pandas as pd
    import matplotlib.pylab as plt
    import numpy as np

    conn = sqlite3.connect('data-20.db')
    cur = conn.cursor()
    cur.execute("select formula,optional_fragment,partial_beb from partial_beb where name='{0}'".format(name))
    rows_1 = cur.fetchall()
    a_formula=rows_1[0][0]
    num_partial_beb = len(rows_1)
    x_70 = [70]*num_partial_beb
    a_df_1 = pd.DataFrame(rows_1,columns=['formula','optional_fragment','partial_beb'])

    plt.figure()
    x = x_70
    y = a_df_1['partial_beb'].values
    plt.scatter(x,y,marker='X', color='coral',label='partial_beb')

    cur.execute("select energy,beb from energy_vs_total_beb where formula='{0}'".format(a_formula))
    rows = cur.fetchall()
    a_df = pd.DataFrame(rows,columns=['energy','total_beb'])
    
    total_beb_70 = a_df[a_df['energy']==70]['total_beb'].values
    plot_other_energy_partial_beb(50,total_beb_70,a_df,num_partial_beb,y)
    plot_other_energy_partial_beb(60,total_beb_70,a_df,num_partial_beb,y)
    plot_other_energy_partial_beb(80,total_beb_70,a_df,num_partial_beb,y)
    plot_other_energy_partial_beb(100,total_beb_70,a_df,num_partial_beb,y)
    plot_other_energy_partial_beb(150,total_beb_70,a_df,num_partial_beb,y)
    plot_other_energy_partial_beb(250,total_beb_70,a_df,num_partial_beb,y)


    x1 = a_df['energy'].values
    y1 = a_df['total_beb'].values
    plt.plot(x1,y1,color='black',label='total_beb')

    plt.xlabel('energy /eV')
    plt.ylabel('ionisation cross sections /$A^2$')
    plt.title('{0} ({1})'.format(name,a_formula))
    plt.xlim(0,300)
    plt.legend()
    if save == True:
        plt.savefig('total_and_partial_ionization_cross_sections_of_{0}'.format(name))
    plt.show()

plot_energy_vs_total_and_partial_beb('Methane',True)
plot_energy_vs_total_and_partial_beb('Tetrafluoromethane')

# %%
import sqlite3
conn = sqlite3.connect('data-20.db')
cur = conn.cursor()
cur.execute("select distinct name from partial_beb")
print('the number of molecule with partial beb at 70eV is' ,len(list(cur)))
cur.execute("select distinct name from energy_vs_total_beb")
print('the number of molecule with total beb at many energy level is' ,len(list(cur)))
cur.execute("select distinct name from appearance_energy_of_all_molecules")
print('the number of molecule with AE is' ,len(list(cur)))
cur.execute("select distinct name from main_data")
print('the number of molecule with original data is' ,len(list(cur)))
conn.close()
# %%
import numpy as np
original_data = np.load('new_data.npy', allow_pickle=True).item()
print(len(original_data),"which is less than the data in the table, because there are some molecules with 'D' in the formula.")
# %%
