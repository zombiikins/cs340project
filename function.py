def delEmptyColumn(requestForm):
  keys = list(requestForm.keys())
  for k in keys:
    if requestForm[k] == '':
      del requestForm[k]
  
  return requestForm

def colNames(requestForm):
  colString = ''

  if len(requestForm) == 1:
    colString = list(requestForm.keys())[0]
  else:
    for k in requestForm.keys():
      colString += k+', '
    
    colString = colString[:-2]

  return colString

def valuesString(requestForm):
  valString = ''

  if len(requestForm) == 1:
    valString = list(requestForm.values())[0]
  else:
    for v in requestForm.values():
      valString += "'"+v+"'"+', '

    valString = valString[:-2]

  return valString

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

def updateString(requestForm):
  updateStr = ''
  for k, v in requestForm.items():
    updateStr += k + ' = ' +  "'" + v + "'" + ', ' 
  
  updateStr = updateStr[:-2]
  return updateStr