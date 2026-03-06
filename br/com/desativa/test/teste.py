from pyspark.sql import SparkSession
from pyspark.sql.functions import col, length

spark = (
    SparkSession
    .builder
    .appName("Exercicios_CSV")
    .getOrCreate()
)

df = spark.read.csv("test.csv", header=True, inferSchema=True, sep=";")

# Exerciser 1
df_name_profession = df.select("firstname", "lastname", "profession").orderBy("profession")
# df_name_profession.show(5)
# +---------+--------+----------+
# |firstname|lastname|profession|
# +---------+--------+----------+
# |Cathyleen| Dawkins| developer|
# |   Noelle|   Cavan| developer|
# |    Adore|  Baudin| developer|
# |   Orelia|  Vacuva| developer|
# |  Ardenia|Francene| developer|

# Exerciser 2
df_developer = df.filter((col("id") > 500) & (col("profession") == "developer"))
# df_developer.show(5)
# +---+---------+--------+--------------------+--------------------+----------+----------+-----------+
# | id|firstname|lastname|               email|              email2|profession|Field Name|Field Name2|
# +---+---------+--------+--------------------+--------------------+----------+----------+-----------+
# |501|  Madalyn| Vernier|Madalyn.Vernier@y...|Madalyn.Vernier@g...| developer|       402|        402|
# |503|    Dania|    Harl|Dania.Harl@yopmai...|Dania.Harl@gmail.com| developer|       404|        404|
# |506|    Rayna|     Wyn|Rayna.Wyn@yopmail...| Rayna.Wyn@gmail.com| developer|       407|        407|
# |507|    Kayla|  Amadas|Kayla.Amadas@yopm...|Kayla.Amadas@gmai...| developer|       408|        408|
# |511|  Gusella|  Lymann|Gusella.Lymann@yo...|Gusella.Lymann@gm...| developer|       412|        412|
# +---+---------+--------+--------------------+--------------------+----------+----------+-----------+

# Exerciser 3
df_profession_emergency = df.filter((col("profession").isin(["police officer", "firefighter"])))
df_profession_emergency = df_profession_emergency.select("firstname", "profession", "email2")
df_profession_emergency.show()
# +---------+--------------+--------------------+
# |firstname|    profession|              email2|
# +---------+--------------+--------------------+
# |  Gaylene|police officer|Gaylene.Alarise@g...|
# |  Celisse|police officer|Celisse.Hessler@g...|
# |  Julieta|police officer|Julieta.Cornelia@...|
# |    Fanny|police officer|Fanny.Kussell@gma...|
# |     Bill|   firefighter|Bill.Dudley@gmail...|

# Exerciser 4
df_size_name = df.withColumn("firstname_size", length(col("firstname")))
df_size_name = df_size_name.select("firstname", "firstname_size")
# df_size_name.show(5)
# +---------+--------------+
# |firstname|firstname_size|
# +---------+--------------+
# |    Johna|             5|
# |  Gaylene|             7|
# | Tomasina|             8|
# |    Shell|             5|
# |   Orelia|             6|
# +---------+--------------+

# Exerciser 5
df_initial = df.withColumn("initial", )
