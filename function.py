def delEmptyColumn(requestForm):
  keys = list(requestForm.keys())
  for k in keys:
    if requestForm[k] == '':
      del requestForm[k]
  
  return requestForm

def colNames(requestForm):
  colstring = ''

  if len(requestForm) == 1:
    colString = list(requestForm.keys())[0]
  else:
    for k in requestForm.keys():
      colstring += k+', '
    
    colstring = colstring[:-2]

  return colstring

def valuesString(requestForm):
  valString = ''

  if len(requestForm) == 1:
    valString = list(requestForm.values())[0]
  else:
    for v in requestForm.values():
      valString += "'"+v+"'"+', '

    valString = valString[:-2]

  return valString