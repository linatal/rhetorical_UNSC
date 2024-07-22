import pandas as pd
import matplotlib.pyplot as plt
import matplotlib


def plot_topics(df_topics):
    matplotlib.style.use('ggplot')
    ax = df_topics.plot(kind="bar")
    plt.xticks(rotation=30, horizontalalignment="center")
    ax.set_ylim(ymin=0, ymax=0.4)

    plt.rc('axes', titlesize=14)
    plt.rc('xtick', labelsize=14)
    plt.rc('ytick', labelsize=14)

    # function to add value labels
    for p in ax.patches:
        ax.annotate(str(round(p.get_height(),2)), (p.get_x() * 1.005, p.get_height() * 1.005))
    plt.title("Tree Structure of Paragraphs per UNSC Topic")
    #plt.xlabel("Distribution Nucluearity Mass (NM)")
    plt.ylabel("Value per Paragraph")
    plt.show()

def plot_topics_confl(df_topics_confl):
    matplotlib.style.use('ggplot')
    ax = df_topics_confl.plot(kind="bar")



    plt.xticks(rotation=30, horizontalalignment="center")
    ax.set_ylim(ymin=0, ymax=0.4)
    #plt.rcParams.update({'font.size': 10})

    plt.rc('axes', titlesize=14)
    plt.rc('xtick', labelsize=20)
    plt.rc('ytick', labelsize=20)

    # function to add value labels
    for p in ax.patches:
        ax.annotate(str(round(p.get_height(),2)), (p.get_x() * 1.005, p.get_height() * 1.005))

    plt.title("Tree Structure of Conflict- and Non-Conflict Paragraphs per UNSC Topic")
    plt.xlabel("Distribution Nucluearity Mass (NM)")
    #plt.ylabel("Value per Paragraph")
    plt.show()

def plot_countries(df_countries):
    matplotlib.style.use('ggplot')
    ax = df_countries.plot(kind="bar")
    plt.xticks(rotation=30, horizontalalignment="center")
    #ax.set_ylim(ymin=0, ymax=0.4)
    # function to add value labels
    for p in ax.patches:
        ax.annotate(str(round(p.get_height(),2)), (p.get_x()* 1.005, p.get_height() * 1.005))

    plt.title("Tree Structure of Conflict- and Non-Conflict Paragraphs per Country")
    plt.xlabel("Distribution of Nucluearity Mass (NM)")
    plt.ylabel("Value per Paragraph")
    plt.show()

def plot_countries_sm(df_countries):
    df_countries = df_countries.drop(['NM1_Conflict', "NM1_Non-Conflict"], axis=0)
    df_countries = df_countries.rename({'NM2_Conflict':'Conflict', "NM2_Non-Conflict":"Non-Conflict"}, axis=0)
    matplotlib.style.use('ggplot')
    ax = df_countries.plot(kind="bar")
    plt.xticks(rotation=30, horizontalalignment="center")
    #ax.set_ylim(ymin=0, ymax=0.4)
    # function to add value labels
    for p in ax.patches:
        ax.annotate(str(round(p.get_height(),2)), (p.get_x()* 1.005, p.get_height() * 1.005))

    plt.title("Tree Structure of Conflict- and Non-Conflict Paragraphs")
    plt.xlabel("Distribution of Nucluearity Mass 2 (NM2)")
    plt.ylabel("Value per Paragraph")
    plt.show()


def compare_topic(df_paragraphs):
    df_ukr = df_paragraphs[df_paragraphs['filename'].str.contains('UNSC_2014')]
    df_wps = df_paragraphs[df_paragraphs['filename'].str.contains('UNSC_2016')]
    print("mean NM1 and NM2 values for Ukraine:")
    print(df_ukr[['NM1_para', 'NM2_para']].mean())
    ukr_topic = df_ukr[['NM1_para', 'NM2_para']].mean().tolist()
    print("mean NM1 and NM2 values for WPS:")
    print(df_wps[['NM1_para', 'NM2_para']].mean())
    wps_topic = df_wps[['NM1_para', 'NM2_para']].mean().tolist()
    df_topics = pd.DataFrame({'Ukraine':ukr_topic, 'WPS':wps_topic})
    df_topics.index = ['NM1', 'NM2']

    plot_topics(df_topics)

    df_ukr_confl = df_ukr[df_ukr['propotion_conflict_para'] >= 0.3]
    df_ukr_noconfl = df_ukr[df_ukr['propotion_conflict_para'] < 0.3]
    df_wps_confl = df_wps[df_wps['propotion_conflict_para'] >= 0.3]
    df_wps_noconfl = df_wps[df_wps['propotion_conflict_para'] < 0.3]

    print("Number of paragraphs being Conflict-heavy (Ukraine)", df_ukr_confl.shape[0])
    print("Number of paragraphs being less Conflict-heavy (Ukraine)", df_ukr_noconfl.shape[0])
    print("Number of paragraphs being Conflict-heavy (WPS)", df_wps_confl.shape[0])
    print("Number of paragraphs being less Conflict-heavy (WPS)", df_wps_noconfl.shape[0])

    print("mean NM1 and NM2 values for Ukraine Conflicts:")
    print(df_ukr_confl[['NM1_para', 'NM2_para']].mean())
    ukr_confl = df_ukr_confl[['NM1_para', 'NM2_para']].mean().tolist()
    print("mean NM1 and NM2 values for Ukraine No-Conflicts:")
    print(df_ukr_noconfl[['NM1_para', 'NM2_para']].mean())
    ukr_noconfl = df_ukr_noconfl[['NM1_para', 'NM2_para']].mean().tolist()

    print("mean NM1 and NM2 values for WPS Conflicts:")
    print(df_wps_confl[['NM1_para', 'NM2_para']].mean())
    wps_confl = df_wps_confl[['NM1_para', 'NM2_para']].mean().tolist()
    print("mean NM1 and NM2 values for WPS No-Conflicts:")
    print(df_wps_noconfl[['NM1_para', 'NM2_para']].mean())
    wps_noconfl = df_wps_noconfl[['NM1_para', 'NM2_para']].mean().tolist()

    df_topics_confl = pd.DataFrame({'Ukraine': ukr_confl+ukr_noconfl, 'WPS': wps_confl+wps_noconfl})
    df_topics_confl.index = ['NM1_Conflict', 'NM2_Conflict', "NM1_Non-Conflict", "NM2_Non-Conflict"]
    df_topics_confl = df_topics_confl.sort_index()

    plot_topics_confl(df_topics_confl)
    print()


def compare_countries(df_paragraphs):

    df_ukraine = df_paragraphs[df_paragraphs['filename'].str.contains('Ukraine')]
    df_ukraine_confl = df_ukraine[df_ukraine['propotion_conflict_para'] >= 0.3]
    df_ukraine_noconfl = df_ukraine[df_ukraine['propotion_conflict_para'] < 0.3]
    df_ru = df_paragraphs[df_paragraphs['filename'].str.contains('Russian_Federation')]
    df_ru_confl = df_ru[df_ru['propotion_conflict_para'] >= 0.3]
    df_ru_noconfl = df_ru[df_ru['propotion_conflict_para'] < 0.3]
    df_usa = df_paragraphs[df_paragraphs['filename'].str.contains('America')]
    df_usa_confl = df_usa[df_usa['propotion_conflict_para'] >= 0.3]
    df_usa_noconfl = df_usa[df_usa['propotion_conflict_para'] < 0.3]
    df_china = df_paragraphs[df_paragraphs['filename'].str.contains('China')]
    df_china_confl = df_china[df_china['propotion_conflict_para'] >= 0.3]
    df_china_noconfl = df_china[df_china['propotion_conflict_para'] < 0.3]
    df_uk = df_paragraphs[df_paragraphs['filename'].str.contains('United_Kingdom_Of_Great_Britain_And_Northern_Ireland')]
    df_uk_confl = df_uk[df_uk['propotion_conflict_para'] >= 0.3]
    df_uk_noconfl = df_uk[df_uk['propotion_conflict_para'] < 0.3]
    df_fr = df_paragraphs[df_paragraphs['filename'].str.contains('France')]
    df_fr_confl = df_fr[df_fr['propotion_conflict_para'] >= 0.3]
    df_fr_noconfl = df_fr[df_fr['propotion_conflict_para'] < 0.3]

    print('Ukraine number Conflict/No Conflicts: ',  df_ukraine_confl.shape[0], df_ukraine_noconfl.shape[0], 'Russia number Conflict-paragraphs: ', df_ru_confl.shape[0], df_ru_noconfl.shape[0],
          'US number Conflict-paragraphs: ', df_usa_confl.shape[0], df_usa_noconfl.shape[0], 'China number Conflict-paragraphs: ', df_china_confl.shape[0], df_china_noconfl.shape[0],
          'UK number Conflict-paragraphs: ', df_uk_confl.shape[0], df_uk_noconfl.shape[0], 'France number Conflict-paragraphs: ', df_fr_confl.shape[0], df_fr_noconfl.shape[0])

    ukr_confl = df_ukraine_confl[['NM1_para', 'NM2_para']].mean().tolist()
    ukr_noconfl = df_ukraine_noconfl[['NM1_para', 'NM2_para']].mean().tolist()

    ru_confl = df_ru_confl[['NM1_para', 'NM2_para']].mean().tolist()
    ru_noconfl = df_ru_noconfl[['NM1_para', 'NM2_para']].mean().tolist()

    usa_confl = df_usa_confl[['NM1_para', 'NM2_para']].mean().tolist()
    usa_noconfl = df_usa_noconfl[['NM1_para', 'NM2_para']].mean().tolist()

    china_confl = df_china_confl[['NM1_para', 'NM2_para']].mean().tolist()
    china_noconfl = df_china_noconfl[['NM1_para', 'NM2_para']].mean().tolist()

    uk_confl = df_uk_confl[['NM1_para', 'NM2_para']].mean().tolist()
    uk_noconfl = df_uk_noconfl[['NM1_para', 'NM2_para']].mean().tolist()

    fr_confl = df_fr_confl[['NM1_para', 'NM2_para']].mean().tolist()
    fr_noconfl = df_fr_noconfl[['NM1_para', 'NM2_para']].mean().tolist()

    df_countries = pd.DataFrame({'China': china_confl+china_noconfl, 'France': fr_confl+fr_noconfl,
                                 'Ukraine': ukr_confl+ukr_noconfl, 'Russian Federation': ru_confl+ru_noconfl,
                                 'United Kigdom': uk_confl+uk_noconfl, 'United States': usa_confl+usa_noconfl})
    df_countries.index = ['NM1_Conflict', 'NM2_Conflict', "NM1_Non-Conflict", "NM2_Non-Conflict"]
    #plot_countries(df_countries)
    plot_countries_sm(df_countries)


def main():
    table_nm_para = pd.read_csv("../data/output/nuclearity_mass_para.csv", index_col=[0])
    table_nm_spch = pd.read_csv("../data/output/nuclearity_mass_speech.csv", index_col=[0])
    compare_topic(table_nm_para)
    #compare_countries(table_nm_para)
    print()


if __name__ =="__main__":
    main()