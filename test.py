from textwrap import dedent

from click.testing import CliRunner
from pyparsing import ParserElement

from aaindexer.cli import main
from aaindexer.models import AaindexRecord
from aaindexer.parser import aaindex_record
from aaindexer.scrape import scrape_parse


def debug(token: ParserElement):
    """
    Recursively puts a token and all its children into debug mode
    """
    for subtoken in token.recurse():
        subtoken.set_debug()
        debug(subtoken)
    return token


def assess_record(record: str) -> AaindexRecord:
    """
    Given a record, preprocesses it and parses it
    """
    record = dedent(record).lstrip()
    debug(aaindex_record)
    return aaindex_record.parse_string(record)[0]


def test_onek900102():
    result = assess_record("""
    H ONEK900102
    D Helix formation parameters (delta delta G) (O'Neil-DeGrado, 1990)
    R PMID:2237415
    A O'Neil, K.T. and DeGrado, W.F.
    T A thermodynamic scale for the helix-forming tendencies of the commonly
      occurring amino acids
    J Science 250, 646-651 (1990)
    C FINA910102    0.964  AVBF000104    0.919  GEOR030109    0.908
      MUNV940105    0.876  MUNV940101    0.861  MUNV940102    0.860
      RACS820114    0.855  MUNV940104    0.845  ISOY800104    0.828
      TANS770104    0.826  QIAN880109   -0.800  PTIO830101   -0.830
      FAUJ880113   -0.839  QIAN880108   -0.860  ROBB760104   -0.861
      ROBB760103   -0.867  BUNA790101   -0.949  BLAM930101   -0.974
      ONEK900101   -0.982
    I    A/L     R/K     N/M     D/F     C/P     Q/S     E/T     G/W     H/Y     I/V
       -0.77   -0.68   -0.07   -0.15   -0.23   -0.33   -0.27    0.00   -0.06   -0.23
       -0.62   -0.65   -0.50   -0.41       3   -0.35   -0.11   -0.45   -0.17   -0.14
    //
    """)

    assert isinstance(result, AaindexRecord)
    assert result.accession == "ONEK900102"
    assert result.description == "Helix formation parameters (delta delta G) (O'Neil-DeGrado, 1990)"
    assert result.pmid == "PMID:2237415"
    assert result.authors == "O'Neil, K.T. and DeGrado, W.F."
    assert result.title == "A thermodynamic scale for the helix-forming tendencies of the commonly occurring amino acids"
    assert result.journal == "Science 250, 646-651 (1990)"
    assert result.correlation["FAUJ880113"] == -0.839
    assert result.correlation["ONEK900101"] == -0.982
    assert result.index["A"] == -0.77
    assert result.index["V"] == -0.14


def test_avbf000101():
    result = assess_record("""
    H AVBF000101
    D Screening coefficients gamma, local (Avbelj, 2000)
    R PMID:10903873
    A Avbelj, F.
    T Amino acid conformational preferences and solvation of polar backbone atoms 
      in peptides and proteins
    J J. Mol. Biol. 300, 1335-1359 (2000) (Pro missing)
    C QIAN880120    0.876  PTIO830102    0.861  KANM800102    0.859
      QIAN880119    0.859  LIFS790101    0.857  QIAN880121    0.855
      CHAM830103    0.843  ROBB760106    0.834  LEVM780105    0.824
      PALJ810104    0.818  PALJ810110    0.816  PRAM900103    0.815
      LEVM780102    0.815  LIFS790103    0.814  AVBF000102    0.805
      LEVM780106   -0.805  GEIM800111   -0.806  QIAN880133   -0.807
      QIAN880132   -0.809  KIMC930101   -0.814  MUNV940104   -0.821
      QIAN880134   -0.822  GEIM800110   -0.825  MUNV940103   -0.917
    I    A/L     R/K     N/M     D/F     C/P     Q/S     E/T     G/W     H/Y     I/V
       0.163   0.220   0.124   0.212   0.316   0.274   0.212   0.080   0.315   0.474
       0.315   0.255   0.356   0.410      NA   0.290   0.412   0.325   0.354   0.515
    //
    """)

    assert result.index["P"] is None


def test_kars160101():
    result = assess_record("""
    H KARS160101
    D Number of vertices (order of the graph) (Karkbara-Knisley, 2016)
    R
    A Karkbara, S. and Knisley, D.
    T A graph-theoretic model of single point mutations in the cystic fibrosis
      transmembrane conductance regulator
    J J. Adv. Biotechnol. Vol.6, No.1, 780-786 (2016)
    C
    I    A/L     R/K     N/M     D/F     C/P     Q/S     E/T     G/W     H/Y     I/V
        2.00    8.00    5.00    5.00    3.00    6.00    6.00    1.00    7.00    5.00
        5.00    6.00    5.00    8.00    4.00    3.00    4.00   11.00    9.00    4.00
    //
    """)
    assert result.correlation is None
    assert result.pmid is None


def test_bens940101():
    result = assess_record("""
    H BENS940101
    D Log-odds scoring matrix collected in 6.4-8.7 PAM (Benner et al., 1994)
    R PMID:7700864
    A Benner, S.A., Cohen, M.A. and Gonnet, G.H.
    T Amino acid substitution during functionally constrained divergent
      evolution of protein sequences
    J Protein Engineering 7, 1323-1332 (1994)
    * extrapolated to 250 PAM
    M rows = ARNDCQEGHILKMFPSTWYV, cols = ARNDCQEGHILKMFPSTWYV
         2.5
        -1.7     5.1
         0.0    -0.1     3.6
        -0.6    -1.5     2.5     5.2
        -1.7    -0.4    -1.6    -3.7    12.1
        -1.7     2.5     0.1     0.6    -3.2     5.3
        -0.7    -0.4     1.1     4.4    -4.7     2.1     5.2
         0.8    -0.1    -0.1     0.8    -1.3    -1.6     0.5     5.8
        -2.1     1.8     1.4     0.1    -1.2     3.2    -0.2    -2.1     6.1
         0.1    -3.8    -2.5    -4.2    -3.6    -3.8    -4.1    -3.4    -3.7     4.4
        -1.3    -3.2    -3.4    -5.3    -3.8    -2.4    -5.0    -4.6    -2.2     2.4     4.8
        -1.9     4.3     1.0    -0.2    -2.8     2.5     0.9    -1.4     0.9    -3.8    -4.1     5.6
        -0.2    -3.0    -2.5    -4.3    -3.7    -3.1    -4.1    -3.7    -3.4     4.0     2.9    -2.9     4.8
        -3.2    -4.9    -3.5    -5.7    -0.1    -4.4    -6.7    -5.7     0.1     0.0     2.4    -6.3    -0.1     8.3
         1.1    -1.3    -1.1    -2.8    -2.7     0.1    -2.6    -1.7    -0.4    -2.0    -0.2    -2.3    -1.8    -3.2     6.5
         1.4    -0.9     1.2    -0.4     0.9    -1.4    -1.2     0.8    -0.9    -1.2    -1.5    -1.2    -1.3    -1.8     1.4     2.1
         1.7    -1.3     0.5    -1.2    -1.5    -1.7    -1.6    -0.5    -1.7     0.7    -0.4    -1.1     0.6    -2.4     0.6     1.5     2.4
        -4.3     2.0    -4.4    -6.3     1.6    -2.6    -5.6    -1.7    -2.8    -5.0    -3.0    -1.4    -4.4    -1.6    -4.8    -2.9    -2.6    14.7
        -4.0    -2.6    -0.9    -2.3     2.6    -1.4    -4.1    -4.9     4.4    -3.3    -1.6    -4.0    -3.6     5.6    -3.8    -1.8    -3.4    -0.3     9.5
         0.7    -3.7    -2.4    -3.3    -3.1    -3.5    -3.0    -2.3    -3.8     3.9     1.9    -3.8     3.3    -0.5    -1.6    -0.9     0.6    -4.8    -3.8     4.0
    //
    """)

    assert result.comment == "extrapolated to 250 PAM"


def test_azae970101():
    result = assess_record("""
    H AZAE970101
    D The single residue substitution matrix from interchanges of
      spatially neighbouring residues (Azarya-Sprinzak et al., 1997)
    R PMID:9488136
    A Azarya-Sprinzak, E., Naor, D., Wolfson, H.J. and Nussinov, R.
    T Interchanges of spatially neighbouring residues in structurally conserved
      environments.
    J Protein Engineering 10, 1109-1122 (1997)
    M rows = ARNDCQEGHILKMFPSTWYV, cols = ARNDCQEGHILKMFPSTWYV
          14
           1      16
           1      10      15
           0      13      16      26
           5      -9      -4      -8      18
           0      16      13      16     -10      21
           2      13      10      15      -8      17      11
           5       0       8       7       1       0       1      24
          -2       4       5       8      -2       6       4       6       7
          -6     -11     -11     -14       2     -12     -11     -10      -4      10
          -2      -8      -9     -11       1      -9      -8      -9      -5       8       9
           1      21      12      16     -11      22      17      -1       3     -13     -10      28
           2      -1      -3      -7       0      -2       1      -3      -1       2       5      -4       2
          -4      -8      -9     -10       2     -10      -7      -4      -1       6       5     -11       2       8
           2       2      11      11       0       1       5      13       4     -14     -12       5     -10      -6      51
           1       6       7       8      -1       6       6       8       3      -8      -7       6      -5      -5       6       9
          -2       5       4       4      -5       6       3       1       4      -4      -6       7      -4      -4       5       5      10
          -2      -3      -5      -5      -1      -3      -6      -1       3       4       2      -8       2       5      -5      -4      -2       8
          -2      -1      -3      -4      -1      -3      -1      -2       0       2       0      -3       1       3      -5      -1       0       2       4
          -5     -11     -11     -13       3     -12     -12      -8      -4       9       5     -14       0       5      -7      -6      -3       4       2      11
    //
    """)

    assert result.matrix["A"]["A"] == 14


def test_mehp950101():
    result = assess_record("""
    H MEHP950101
    D (Mehta et al., 1995)
    R PMID:8580842
    A Mehta, P.K., Heringa, J. and Argos, P.
    T A simple and fast approach to prediction of protein secondary structure from
      multiply aligned sequences with accuracy above 70%
    J Protein Science 4, 2517-2525 (1995)
    M rows = ARNDCQEGHILKMFPSTWYV, cols = ARNDCQEGHILKMFPSTWYV
        1.23
        1.17    1.06
        1.28    1.03    1.02
        1.31    1.18    1.08    1.11
        1.41    1.21    1.36    1.44    1.04
        1.31    1.10    1.20    1.25    1.49    1.16
        1.34    1.15    1.21    1.31    1.43    1.26    1.19
        1.11    0.99    0.96    1.02    1.36    1.11    1.06    0.86
        1.17    1.06    1.13    1.05    1.50    1.22    1.23    1.10    0.99
        1.08    0.91    0.89    0.93    1.24    1.02    0.96    0.79    0.86    0.90
        1.19    1.02    0.98    1.00    1.41    1.01    1.01    0.88    1.08    0.99    1.04
        1.29    1.11    1.14    1.18    1.31    1.21    1.22    1.05    1.10    0.94    1.07    1.13
        1.20    0.97    1.01    0.94    1.36    1.10    1.02    0.81    1.08    1.01    1.08    0.99    1.04
        0.94    0.74    0.83    0.79    1.16    0.88    0.91    0.68    0.94    0.74    0.90    0.78    0.91    0.82
        0.94    0.69    0.74    0.84    1.30    0.91    0.96    0.92    0.80    0.67    0.75    0.67    0.59    0.69    0.75
        1.17    0.90    1.01    0.97    1.33    1.09    1.02    0.94    1.03    0.89    1.01    0.98    0.59    0.78    0.79    0.93
        1.06    0.88    0.93    1.01    1.18    1.02    0.94    0.86    0.95       -    0.90    0.88    0.96    0.72    0.80    0.87    0.85
        0.90    0.63    0.88    0.87    0.78    0.95    0.86    0.58    0.92    0.53    0.72    0.74    0.75    0.66    0.40    0.69    0.74    0.91
        0.86    0.75    0.83    0.73    1.00    0.85    0.76    0.58    0.81    0.68    0.79    0.79    0.86    0.71    0.54    0.63    0.65    0.66    0.80
        1.09    0.98    0.96    1.01    1.33    1.06    1.04    0.95    1.01    0.83    0.88    0.99    1.02    0.76    0.77    0.93    0.84    0.60    0.67    0.83
    //
    """)
    assert result.matrix["T"]["I"] is None


def test_kosj950101():
    result = assess_record("""
    H KOSJ950101
    D Context-dependent optimal substitution matrices for exposed helix
      (Koshi-Goldstein, 1995)
    R PMID:8577693
    A Koshi, J.M. and Goldstein, R.A.
    T Context-dependent optimal substitution matrices.
    J Protein Engineering 8, 641-645 (1995)
    M rows = -ARNDCQEGHILKMFPSTWYV, cols = -ARNDCQEGHILKMFPSTWYV
       55.7    3.0    3.0    3.0    3.0    0.4    0.1    3.0    3.0    2.1    3.0    3.0    3.0    0.1    1.9    2.2    2.4    3.0    0.8    1.3    3.0
       25.6   47.2    1.5    1.0    0.7    0.3    1.9    2.3    4.3    0.6    0.2    2.0    0.8    0.1    0.3    3.1    2.8    3.7    0.4    0.1    2.0
       14.8    0.9   62.7    1.3    0.4    0.3    4.6    0.3    0.1    1.9    0.5    2.2    5.1    0.6    0.2    0.4    1.9    1.5    0.4    0.2    0.3
       15.2    0.2    0.5   48.2    3.3    0.1    3.2    4.9    0.1    1.7    1.7    1.4    3.0    0.6    1.0    0.1    9.7    2.7    0.7    1.1    1.5
       15.9    3.9    1.4    7.3   52.1    0.3    0.9   11.0    2.0    0.4    0.6    0.1    0.6    0.5    0.1    0.6    2.9    0.1    0.1    0.1    0.1
        9.4    1.5    0.1    1.5    1.6   73.6    0.1    2.6    0.1    0.1    2.1    4.0    0.1    0.1    0.8    0.7    0.3    2.2    0.1    0.1    0.1
        0.1    8.4    5.7    2.0    4.5    0.3   47.5    8.2    0.9    1.6    0.1    3.4    7.8    0.5    0.1    0.7    5.3    2.2    0.2    0.7    0.5
        5.2    5.3    1.0    1.5    8.6    0.1    4.9   56.8    1.5    1.0    0.3    0.9    5.8    0.1    0.2    1.6    2.1    2.4    0.2    0.1    1.1
       20.2    2.0    1.2    2.3    3.3    0.1    0.4    0.1      6    4.8    0.8    0.1    0.1    1.4    0.3    0.6    0.1    1.2    0.6    0.1    0.5
       13.3    0.3    4.7    7.5    1.8    0.1    4.4    0.7    0.1   56.9    0.6    0.1    2.3    1.2    2.2    0.1    0.1    0.1    0.1    4.4    0.1
       18.4    0.1    0.1    0.1    0.1    0.1    0.4    0.1    0.1    0.1      5    2.6   10.8    1.2    3.5    1.3    0.1    0.1    3.4    0.1    0.1
       15.4    0.8    0.6    0.1    0.1    0.1    1.1    0.1    0.2    0.2    3.4   67.3    0.6    3.5    3.5    0.1    0.1    0.7    0.1    0.1    2.9
        5.5    4.1    8.3    3.5    1.3    0.1    3.7    5.8    1.1    1.2    0.3    1.0   55.3    0.4    0.1    0.2    2.7    3.7    0.1    0.2    1.9
        0.7    5.2    4.3    3.2    0.1    0.5    2.0    5.4    1.5    0.1    7.4    9.3    3.0   44.0    1.3    0.1    2.4    4.3    0.1    0.1    6.0
       14.3    1.7    0.1    0.3    0.5    1.0    0.8    0.5    0.1    0.1    0.7    1.5    0.1    0.4   67.6    0.1    2.1    1.8    0.1    7.1    0.1
       13.6    1.7    1.0    0.5    3.1    0.1    0.6    0.6    0.1    1.0    0.8    1.5    2.7    0.1    0.1   65.9    5.2    1.8    0.1    0.3    0.2
        6.0   18.1    1.2    1.6    2.7    0.9    0.4    2.4    5.0    1.1    0.6    0.2    3.5    0.1    0.1    0.5   46.8    7.5    0.1    0.5    1.4
       18.4    7.5    0.3    2.5    0.7    0.1    0.4    0.2    1.8    0.8    2.4    4.8    1.2    1.0    0.1    0.2    6.3   48.8    0.1    0.6    2.7
       21.7    0.3    0.1    0.1    0.1    0.1    1.8    0.1    0.1    0.1    0.1    2.1    2.5    0.1    4.3    0.1    0.1    0.6   64.6    2.3    0.1
        8.3    0.5    0.1    0.1    0.1    0.1    0.1    1.1    0.1    3.4    2.4    6.6    0.9    0.2    8.7    0.3    0.9    1.5    1.0   60.8    3.8
       14.2    6.2    1.4    0.7    0.1    0.1    0.1    0.3    0.3    0.1   17.5    1.9    0.1    0.1    1.6    0.2    0.1    0.6    0.3    1.2   53.9
    //
    """)

    assert result.matrix["-"]["-"] == 55.7


def test_aaindex_1():
    db = scrape_parse(1)
    assert isinstance(db, list)
    assert len(db) == 566


def test_aaindex_2():
    db = scrape_parse(2)
    assert isinstance(db, list)
    assert len(db) == 94


def test_aaindex_3():
    db = scrape_parse(3)
    assert isinstance(db, list)
    assert len(db) == 47


def test_cli():
    runner = CliRunner()
    result = runner.invoke(main, ["3", "--pretty"], catch_exceptions=True)
    assert result.exit_code == 0, result.exception
