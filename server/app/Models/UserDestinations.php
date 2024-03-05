<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class UserDestinations extends Model
{
    use HasFactory;

    protected $primaryKey = "destination_id";

    protected $fillable = [
        "destination_id",
        "plan_id",
        "user_id",
        "destination_name",
        "destination_datetime"
    ];

}
