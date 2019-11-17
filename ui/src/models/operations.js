export class CreateOrUpdateOperation{
    constructor(object) {
        this.operation_object = object
    }
}

export class DeleteOperation {
    constructor(objectId) {
        this.object_id = objectId
    }
}
