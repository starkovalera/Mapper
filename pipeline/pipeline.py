def pipeline(reader, mapper, writer):
    for batch in reader.read():
        writer.write(mapper.map(item) for item in batch)
