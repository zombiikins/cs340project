# this file contain several help functions to concatenate the query string

# function to delete the key has no value
def delEmptyColumn(requestForm):
  keys = list(requestForm.keys())
  for k in keys:
    if requestForm[k] == '':
      del requestForm[k]
  
  return requestForm

# function to return a string like:
# key1, key2, ... keyN
def colNames(requestForm):
  colString = ''

  if len(requestForm) == 1:
    colString = list(requestForm.keys())[0]
  else:
    for k in requestForm.keys():
      colString += k+', '
    
    colString = colString[:-2]

  return colString

# function to return a string like:
# 'val1', 'val2', ... 'valN'
def valuesString(requestForm):
  valString = ''

  if len(requestForm) == 1:
    valString = list(requestForm.values())[0]
  else:
    for v in requestForm.values():
      valString += "'"+v+"'"+', '

    valString = valString[:-2]

  return valString

# function to return a string like:
# key1 = 'val1' AND key2 = 'val2' AND ... keyN = 'valN'
def conditionString(requestForm):
  conString = ''

  if len(requestForm) == 1:
    for k, v in requestForm.items():
      conString = k + ' = ' + "'" + v + "'"
  else:
    for k, v in requestForm.items():
      conString += k + ' = ' +  "'" + v + "'" + ' AND '
    
    conString = conString[:-5]

  return conString

# function to return a string like:
# key1 = 'val1', key2 = 'val2', ... keyN = 'valN'
def updateString(requestForm):
  updateStr = ''
  for k, v in requestForm.items():
    if v == None:
      updateStr += k + ' = ' + ' NULL' + ', '
    elif v == '':
      updateStr += k + ' = ' + ' NULL' + ', '
    else:
      updateStr += k + ' = ' +  "'" + v + "'" + ', ' 
  
  updateStr = updateStr[:-2]
  return updateStr
